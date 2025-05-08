import pytest
from flask import Flask
from flask_restx import Api
from server.auth import auth_ns
import data.people as ppl
import data.db_connect as dbc

TEST_EMAILS = [
    "testuser@example.com",
    "duplicate@example.com",
    "loginuser@example.com",
    "wrongpass@example.com",
    "norole@example.com"
]

def create_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    api = Api(app)
    api.add_namespace(auth_ns, path="/auths")
    return app

@pytest.fixture
def client():
    dbc.connect_db()
    for email in TEST_EMAILS:
        try:
            ppl.delete_person(email)
        except:
            pass  
    app = create_app()
    with app.test_client() as client:
        yield client
    for email in TEST_EMAILS:
        try:
            ppl.delete_person(email)
        except:
            pass  

def test_valid_register(client):
    """Test successful registration with valid data."""
    email = "testuser@example.com"
    data = {
        "email": email,
        "password": "testpassword",
        "role": "AU"
    }
    resp = client.post("/auths/registers", json=data)
    assert resp.status_code == 201
    resp_json = resp.get_json()
    assert resp_json["message"] == "User registered successfully."
    
    user = ppl.read_one(email)
    assert user is not None
    assert user["email"] == email
    assert "AU" in user["roles"]

def test_invalid_register_existing_email(client):
    """Test registration with an email that already exists."""
    email = "duplicate@example.com"
    data = {
        "email": email,
        "password": "testpassword",
        "role": "AU"
    }

    resp1 = client.post("/auths/registers", json=data)
    assert resp1.status_code == 201
    
    resp2 = client.post("/auths/registers", json=data)
    assert resp2.status_code == 400
    resp2_json = resp2.get_json()
    assert "User with that email already exists." in resp2_json.get("message", "")

def test_valid_login(client):
    """Test successful login with valid credentials."""
    email = "loginuser@example.com"
    registration_data = {
        "email": email,
        "password": "testpassword",
        "role": "AU"
    }

    resp_reg = client.post("/auths/registers", json=registration_data)
    assert resp_reg.status_code == 201
    login_data = {
        "email": email,
        "password": "testpassword"
    }
    resp_login = client.post("/auths/logins", json=login_data)
    assert resp_login.status_code == 200
    resp_login_json = resp_login.get_json()
    assert resp_login_json["message"] == "Logged in successfully."
    assert "token" in resp_login_json and resp_login_json["token"]

def test_invalid_login_wrong_password(client):
    """Test login with incorrect password."""
    email = "wrongpass@example.com"
    registration_data = {
        "email": email,
        "password": "correctpassword",
        "role": "AU"
    }
    resp_reg = client.post("/auths/registers", json=registration_data)
    assert resp_reg.status_code == 201
    login_data = {
        "email": email,
        "password": "wrongpassword"
    }
    resp_login = client.post("/auths/logins", json=login_data)
    assert resp_login.status_code == 401
    resp_login_json = resp_login.get_json()
    assert "Invalid email or password." in resp_login_json.get("message", "")

def test_invalid_login_nonexistent_user(client):
    """Test login with email that doesn't exist."""
    email = "nonexistent@example.com"
    login_data = {
        "email": email,
        "password": "anypassword"
    }
    resp_login = client.post("/auths/logins", json=login_data)
    assert resp_login.status_code == 401
    resp_login_json = resp_login.get_json()
    assert "Invalid email or password." in resp_login_json.get("message", "")

def test_register_without_role(client):
    """Test registration without specifying a role."""
    email = "norole@example.com"
    data = {
        "email": email,
        "password": "testpassword",
        "role": "AU"  
    }
    resp = client.post("/auths/registers", json=data)
    assert resp.status_code == 201
    resp_json = resp.get_json()
    assert resp_json["message"] == "User registered successfully."
    user = ppl.read_one(email)
    assert user is not None
    assert user["email"] == email
    assert "AU" in user["roles"]

@pytest.mark.parametrize("role", [
    "AU",
    "ED",
    "ME",
    "CE",
    "RE"
])
def test_register_with_various_roles(client, role):
    """Test registration with different roles."""
    email = f"{role.lower()}@example.com"
    
    try:
        ppl.delete_person(email)
    except:
        pass
    
    payload = {
        "email": email,
        "password": "pw1234",
        "role": role
    }
    expected = [role]

    resp = client.post("/auths/registers", json=payload)
    assert resp.status_code == 201
    
    user = ppl.read_one(email)
    assert user is not None
    assert user["roles"] == expected
    
    try:
        ppl.delete_person(email)
    except:
        pass