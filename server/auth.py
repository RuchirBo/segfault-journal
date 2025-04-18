from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
import data.db_connect as db_connect
# import jwt
# from datetime import datetime, timedelta
from security.security import COLLECT_NAME, PEOPLE

auth_ns = Namespace('auth', description="Authentication operations")

SECRET_KEY = "dummy_secret_key"

register_model = auth_ns.model(
    'Register',
    {
        'email': fields.String(
            required=True,
            description="User email"
        ),
        'password': fields.String(
            required=True,
            description="User password"
        ),
        'role': fields.String(
            required=False,
            description="Role code"
        ),
        'role_key': fields.String(
            required=False,
            description="Special key if required by role"
        ),
    }
)

login_model = auth_ns.model(
    'Login',
    {
        'email': fields.String(
            required=True,
            description="User email"
        ),
        'password': fields.String(
            required=True,
            description="User password"
        ),
        'role_key': fields.String(
            required=False,
            description="Special key if required by role"
        ),
    }
)

ROLE_KEYS = {
    'dev': 'segfault',
    'EDITOR': 'EDITOR',
    'CONSULTING_EDITOR': 'CE',
    'AUTHOR': 'AUTHOR',
    'MANAGING_EDTIOR': 'ME',
    'REFEREE': 'REF',
}


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'AU')
        role_key = data.get('role_key', '')

        db_connect.connect_db()

        query = {
            'type': PEOPLE,
            'email': email,
        }
        existing_user = db_connect.fetch_one(COLLECT_NAME, query)

        if existing_user:
            auth_ns.abort(400, "User with that email already exists.")

        if role in ROLE_KEYS:
            if role_key != ROLE_KEYS[role]:
                auth_ns.abort(403, f"Invalid key for role '{role}'")

        hashed_password = generate_password_hash(password)

        user_doc = {
            'type': PEOPLE,
            'email': email,
            'password': hashed_password,
            'role': role
        }

        db_connect.create(COLLECT_NAME, user_doc)
        return {"message": "User registered successfully."}, 201


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role_key = data.get('role_key', '')

        db_connect.connect_db()

        query = {
            'type': PEOPLE,
            'email': email,
        }
        user = db_connect.fetch_one(COLLECT_NAME, query)

        if not user:
            auth_ns.abort(401, "Invalid email or password.")

        stored_password = user.get('password')
        if not check_password_hash(stored_password, password):
            auth_ns.abort(401, "Invalid email or password.")

        user_role = user.get('role', 'AU')
        if user_role in ROLE_KEYS:
            if role_key != ROLE_KEYS[user_role]:
                auth_ns.abort(403, f"Invalid key for role '{user_role}'")

        # payload = {
        #     'email': email,
        #     'role': user_role,
        #     'exp': datetime.utcnow() + timedelta(hours=2)
        # }
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        token = "segfault_dummy_val"

        return {"message": "Logged in successfully.", "token": token}, 200
