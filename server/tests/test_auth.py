import pytest
from flask import Flask
from flask_restx import Api
from server.auth import auth_ns
from security.security import delete_acc
import data.db_connect as db_connect

TEST_EMAILS = [
    "testuser@example.com",
    "duplicate@example.com",
    "loginuser@example.com",
    "wrongpass@example.com"
]

def create_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    api = Api(app)
    api.add_namespace(auth_ns, path="/auth")
    return app

@pytest.fixture
def client():
    db_connect.connect_db()
    for email in TEST_EMAILS:
        delete_acc(email)
    app = create_app()
    with app.test_client() as client:
        yield client
    for email in TEST_EMAILS:
        delete_acc(email)

def test_valid_register(client):
    email = "testuser@example.com"
    data = {
        "email": email,
        "password": "testpassword",
        "role": "dev",
        "role_key": "segfault"
    }
    resp = client.post("/auth/register", json=data)
    assert resp.status_code == 201
    resp_json = resp.get_json()
    assert "message" in resp_json
    assert resp_json["message"] == "User registered successfully."
    delete_acc(email)

def test_invalid_register_existing_email(client):
    email = "duplicate@example.com"
    data = {
        "email": email,
        "password": "testpassword",
        "role": "dev",
        "role_key": "segfault"
    }
    resp1 = client.post("/auth/register", json=data)
    assert resp1.status_code == 201
    resp2 = client.post("/auth/register", json=data)
    assert resp2.status_code == 400
    resp2_json = resp2.get_json()
    assert "User with that email already exists." in resp2_json.get("message", "")
    delete_acc(email)

def test_valid_login(client):
    email = "loginuser@example.com"
    registration_data = {
        "email": email,
        "password": "testpassword",
        "role": "dev",
        "role_key": "segfault"
    }
    resp_reg = client.post("/auth/register", json=registration_data)
    assert resp_reg.status_code == 201

    login_data = {
        "email": email,
        "password": "testpassword",
        "role_key": "segfault"
    }
    resp_login = client.post("/auth/login", json=login_data)
    assert resp_login.status_code == 200
    resp_login_json = resp_login.get_json()
    assert "message" in resp_login_json
    assert "token" in resp_login_json
    assert resp_login_json["token"]
    delete_acc(email)

def test_invalid_login_wrong_password(client):
    email = "wrongpass@example.com"
    registration_data = {
        "email": email,
        "password": "correctpassword",
        "role": "dev",
        "role_key": "segfault"
    }
    resp_reg = client.post("/auth/register", json=registration_data)
    assert resp_reg.status_code == 201

    login_data = {
        "email": email,
        "password": "wrongpassword",
        "role_key": "segfault"
    }
    resp_login = client.post("/auth/login", json=login_data)
    assert resp_login.status_code == 401
    resp_login_json = resp_login.get_json()
    assert "Invalid email or password." in resp_login_json.get("message", "")
    delete_acc(email)
