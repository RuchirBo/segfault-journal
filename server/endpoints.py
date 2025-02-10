"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request  # , request
from flask_restx import Resource, Api, fields  # Namespace, fields
from flask_cors import CORS

import werkzeug.exceptions as wz

import data.people as ppl
import data.manuscripts.query as manu
import data.manuscripts.fields as flds


app = Flask(__name__)
CORS(app)
api = Api(app)

DATE = '2024-09-24'
DATE_RESP = 'Date'
EDITOR = 'ejc369@nyu.edu'
EDITOR_RESP = 'Editor'
ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
MESSAGE = 'Message'
PEOPLE_EP = '/people'
PUBLISHER = 'Segfaulters'
PUBLISHER_RESP = 'Publisher'
TITLE_EP = '/title'
TITLE_RESP = "Title"
RETURN = 'return'
TITLE = 'Segfault Journal Bimonthly'
MANU_EP = '/manuscripts'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route(ENDPOINT_EP)
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(TITLE_EP)
class JournalTitle(Resource):
    """
    This class handles CRUD for the journal title
    """
    def get(self):
        """
        Retrieve the journal title
        """
        return {TITLE_RESP: TITLE}


@api.route(PEOPLE_EP)
class People(Resource):
    """
    This class handles creating, reading, updating, and deleting journal people
    """
    def get(self):
        """
        Retrieve the journal people.
        """
        return ppl.read()

    # def create_person(self, name: str, affiliation: str, email: str):
    #     return ppl.create_person(name, affiliation, email)

    # def delete_person(self, _id):
    #     return ppl.delete_person(_id)


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.String,
})


@api.route(f'{PEOPLE_EP}/create')
class PeopleCreate(Resource):
    """
    Add a person to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self):
        """
        Add a person.
        """
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            role = request.json.get(ppl.ROLES)
            ret = ppl.create_person(name, affiliation, email, role)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person added!',
            RETURN: ret,
        }


# testing
PEOPLE_UPDATE_FIELDS = api.model('UpdatePersonEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.String,
})


@api.route(f'{PEOPLE_EP}/update')
class PeopleUpdate(Resource):
    """
    Update a person in the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_UPDATE_FIELDS)
    def put(self):
        """
        Update a person.
        """
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            roles = request.json.get(ppl.ROLES)
            ppl.update_users(name, affiliation, email, roles)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person updated!',
        }


@api.route(f'{PEOPLE_EP}/<string:email>/delete')
class PeopleDelete(Resource):
    """
    Delete a person from the journal db.
    """
    @api.doc(params={'email': 'Email of person to delete'})
    def delete(self, email):
        try:
            person = ppl.read_one(email)
            if not person:
                raise wz.NotFound(f"No such person: {email}")
            ppl.delete_person(email)
            return {
                "message": f"Person with email {email} was removed."
            }, 200
        except ValueError as e:
            return {"message": str(e)}, 400


MASTHEAD = 'Masthead'


@api.route(f'{PEOPLE_EP}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD: ppl.get_masthead()}


@api.route(f'{PEOPLE_EP}/<string:email>')
class Person(Resource):
    def get(self, email):
        """Retrieve a specific person by email."""
        person = ppl.read_one(email)
        if person:
            return person
        else:
            raise wz.NotFound(f"No such person: {email}")


@api.route(f"{PEOPLE_EP}/<string:email>/roles")
class PersonRoles(Resource):
    @api.doc(params={'role': 'Role to add'})
    def post(self, email):
        """
        Add a role to a person by email and role as query parameters.
        """
        try:
            role = request.args.get('role')
            if not role:
                return {"message": "Role is required."}, 400
            person = ppl.read_one(email)
            if not person:
                return {
                    "message": f"Person with email {email} not found."
                }, 404
            ppl.add_role_to_person(email, role)
            return {
                "message": f"Role '{role}' added to {email}."
            }, 200
        except ValueError as e:
            return {"message": str(e)}, 400

    @api.doc(params={'role': 'Role to remove'})
    def delete(self, email):
        """
        Remove a role from a person by email and role as query parameters.
        """
        try:
            role = request.args.get('role')
            if not role:
                return {"message": "Role is required."}, 400
            person = ppl.read_one(email)
            if not person:
                return {
                    "message": f"Person with email {email} not found."
                }, 404
            ppl.delete_role_from_person(email, role)
            return {
                "message": f"Role '{role}' removed from {email}."
            }, 200
        except ValueError as e:
            return {"message": str(e)}, 400


@api.route(f"{MANU_EP}")
class Manuscripts(Resource):
    def get(self):
        manuscripts = manu.get_all_manuscripts()
        return {'manuscripts': manuscripts}


MANU_CREATE_FLDS = api.model('ManuscriptEntry', {
    flds.TITLE: fields.String,
    flds.AUTHOR: fields.String,
    flds.REFEREES: fields.List(fields.String),
})


@api.route(f'{MANU_EP}/create')
class ManuscriptsCreate(Resource):
    """
    Add a manuscript to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable manuscript data')
    @api.expect(MANU_CREATE_FLDS)
    def put(self):
        """
        Add a manuscript.
        """
        try:
            title = request.json.get(flds.TITLE)
            author = request.json.get(flds.AUTHOR)
            referees = request.json.get(flds.REFEREES, [])
            manuscript = {
                flds.TITLE: title,
                flds.AUTHOR: author,
                flds.REFEREES: referees,
            }
            manu.create_manuscript(manuscript)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add manuscript: '
                                   f'{err=}')
        return {
            MESSAGE: 'Manuscript added!',
        }


MANU_UPDATE_FIELDS = api.model('UpdateManuscriptEntry', {
    'old_manuscript': fields.Nested(MANU_CREATE_FLDS),
    'new_manuscript': fields.Nested(MANU_CREATE_FLDS)
})


@api.route(f'{MANU_EP}/update')
class ManuscriptsUpdate(Resource):
    """
    Update a manuscript in the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_UPDATE_FIELDS)
    def put(self):
        """
        Update a manuscript.
        """
        try:
            old_manuscript = request.json.get("old_manuscript")
            new_manuscript = request.json.get("new_manuscript")
            if not old_manuscript or not new_manuscript:
                raise wz.NotAcceptable('Both the old and new manuscript \
                                       must be provided.')
            manu.update_manuscript(old_manuscript, new_manuscript)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not update manuscript: '
                                   f'{err=}')
        return {
            MESSAGE: 'Manuscript updated!',
        }


MANU_DELETE_FIELDS = api.model('DeleteManuscriptEntry', {
    flds.TITLE: fields.String,
    flds.AUTHOR: fields.String,
})


@api.route(f'{MANU_EP}/delete')
class ManuscriptsDelete(Resource):
    """
    Delete a manuscript from the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_DELETE_FIELDS)
    def delete(self):
        try:
            del_manuscript = request.get_json()
            if not del_manuscript:
                raise ValueError('Missing valid manuscript to delete.')
            title = del_manuscript.get(flds.TITLE)
            author = del_manuscript.get(flds.AUTHOR)

            if not title or not author:
                raise wz.NotAcceptable('Both title and author \
                                       are required for manuscript \
                                       to be deleted.')

            manu.delete_manuscript(title, author)

        except Exception as err:
            raise wz.NotAcceptable(f'Could not delete manuscript: '
                                   f'{err=}')
        return {
            MESSAGE: 'Manuscript deleted!',
        }


MANU_ACTION_FLDS = api.model('ManuscriptAction', {
    manu.MANU_ID: fields.String,
    manu.CURR_STATE: fields.String,
    manu.ACTION: fields.String,
    manu.REFEREE: fields.String,
})


@api.route(f'{MANU_EP}/receive_action')
class ReceiveAction(Resource):
    """
    Receive an action for a manuscript.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_ACTION_FLDS)
    def put(self):
        """
        Receive an action for a manuscript.
        """
        try:
            manu_id = request.json.get(manu.MANU_ID)
            curr_state = request.json.get(manu.CURR_STATE)
            action = request.json.get(manu.ACTION)
            kwargs = {}
            kwargs[manu.REFEREE] = request.json.get(manu.REFEREE)
            ret = manu.handle_action(manu_id, curr_state, action, **kwargs)
        except Exception as err:
            raise wz.NotAcceptable(f'Bad action: ' f'{err=}')
        return {
            MESSAGE: 'Action received!',
            RETURN: ret,
        }