from flask import request, session
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
import data.db_connect as db_connect
# import jwt
# from datetime import datetime, timedelta
from security.security import COLLECT_NAME, PEOPLE
import data.people as ppl

auth_ns = Namespace('auth', description="Authentication operations")

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
    }
)


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', ' ')
        name = email.split('@')[0]
        affiliation = ''  
        roles = [role] if role else []

        existing = ppl.exists(email)  
        if existing:
            auth_ns.abort(400, "User with that email already exists.")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        ppl.create_person(name, affiliation, email, roles)

        return {"message": "User registered successfully."}, 201


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')


        user = ppl.exists(email)  
        # if (not user or
        #         not check_password_hash(user.get('password', ''), password)):
        if(not user):
            auth_ns.abort(401, "Invalid email or password.")

        token = "segfault_dummy_val"

        session['user'] = {
            'email': email,
            'role': ppl.get_person_roles(email)
            # 'role': user.get('role', ' ')
        }

        return {
            "message": "Logged in successfully.",
            "token": token
        }, 200


@auth_ns.route('/user')
class CurrentUser(Resource):
    def get(self):
        user = session.get('user')
        if not user:
            auth_ns.abort(401, "Not logged in.")
        return user, 200


@auth_ns.route('/logout')
class Logout(Resource):
    def post(self):
        session.pop('user', None)
        return {"message": "Logged out successfully."}, 200
