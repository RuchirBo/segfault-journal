"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request  # , request
from flask_restx import Resource, Api, fields  # Namespace, fields
from flask_cors import CORS
from data.manuscripts.manuscript import STATE_DESCRIPTIONS
import subprocess
import werkzeug.exceptions as wz

import data.people as ppl
# import data.manuscripts.query as manu
# import data.manuscripts.fields as flds
import data.manuscripts.manuscript as manu
import data.text as txt
import data.roles as rls
import random

from .auth import auth_ns

app = Flask(__name__)
CORS(app)
api = Api(app)


api.add_namespace(auth_ns, path='/auth')


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
TEXT_EP = '/text'
ROLES_EP = '/roles'
ELOG_LOC= '/var/log/segfault.pythonanywhere.com.error.log'
ELOG_KEY = 'error_log'



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


@api.route(ROLES_EP)
class Roles(Resource):
    """
    This class handles reading person roles.
    """
    def get(self):
        """
        Retrieve the journal person roles.
        """
        return rls.read()


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
    ppl.ROLES: fields.List(fields.String),
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
            roles = request.json.get(ppl.ROLES, [])
            ret = ppl.create_person(name, affiliation, email, roles)
        except Exception as err:
            raise wz.NotAcceptable(f'{str(err)}')
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


@api.route(f'{PEOPLE_EP}/update/<string:email>')
class PeopleUpdate(Resource):
    """
    Update a person in the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_UPDATE_FIELDS)
    def put(self, email):
        """
        Update a person.
        """
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            roles = request.json.get(ppl.ROLES)
            ppl.update_users(name, affiliation, email, roles)
        except Exception as err:
            raise wz.NotAcceptable(f'{str(err)}')
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
            print(f"{person=}")
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
        for manuscript in manuscripts:
            curr_desc = STATE_DESCRIPTIONS.get(manuscript["state"])
            manuscript["state_description"] = curr_desc
        print(manuscripts)
        return {'manuscripts': manuscripts}


@api.route(f"{MANU_EP}/valid")
class ManuscriptsValid(Resource):
    def get(self):
        manuscripts = manu.get_all_valid_manuscripts()
        for manuscript in manuscripts:
            curr_desc = STATE_DESCRIPTIONS.get(manuscript["state"])
            manuscript["state_description"] = curr_desc
        print(manuscripts)
        return {'manuscripts': manuscripts}


MANU_CREATE_FLDS = api.model('ManuscriptEntry', {
    manu.MANU_ID: fields.String,
    manu.TITLE: fields.String,
    manu.AUTHOR_EMAIL: fields.String,
    manu.TEXT: fields.String,
    manu.ABSTRACT: fields.String,
    manu.EDITOR: fields.String
    # manu.REFEREES: fields.List(fields.String),
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
            manu_id = request.json.get(manu.MANU_ID)
            title = request.json.get(manu.TITLE)
            author_email = request.json.get(manu.AUTHOR_EMAIL)
            text = request.json.get(manu.TEXT)
            abstract = request.json.get(manu.ABSTRACT)
            editor = request.json.get(manu.EDITOR)
            # referees = request.json.get(manu.REFEREES, [])
            manuscript = {
                manu.MANU_ID: manu_id,
                manu.TITLE: title,
                manu.AUTHOR_EMAIL: author_email,
                manu.TEXT: text,
                manu.ABSTRACT: abstract,
                manu.EDITOR: editor
                # manu.REFEREES: referees,
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


@api.route(f"{MANU_EP}/<string:title>")
class GetManuscriptByTitle(Resource):
    """
    Retrieve a specific manuscript by title for frontend.
    """
    def get(self, title):
        try:
            manuscript = manu.get_manuscript_by_title(title)
            return manuscript
        except ValueError as err:
            raise wz.NotFound(str(err))


MANU_DELETE_FIELDS = api.model(
    'DeleteManuscriptEntry',
    {
        manu.MANU_ID: fields.String(
            required=True,
            description='Unique manuscript identifier'
        ),
    }
)


@api.route(f'{MANU_EP}/delete')
class ManuscriptsDelete(Resource):
    """
    Delete a manuscript from the journal db by its manuscript_id.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Bad request')
    @api.expect(MANU_DELETE_FIELDS)
    def delete(self):
        body = request.get_json() or {}
        manu_id = body.get(manu.MANU_ID)
        if not manu_id:
            raise wz.NotAcceptable('manuscript_id is required for deletion')
        try:
            manu.delete_manuscript(manu_id)
        except ValueError as e:
            raise wz.NotFound(str(e))
        return {MESSAGE: 'Manuscript deleted!'}, HTTPStatus.OK


@api.route(f"{MANU_EP}/actions/<string:state>")
class GetValidActions(Resource):
    """
    Retrieve all valid actions from a state.
    """
    def get(self, state):
        try:
            if not manu.is_valid_state(state):
                raise wz.NotFound(f"Invalid State: {state}")
            acts = manu.get_valid_actions_by_state(state)
            return {"valid_actions": acts}
        except ValueError as err:
            raise wz.NotFound(str(err))


MANU_ACTION_FLDS = api.model('ManuscriptAction', {
    manu.TITLE: fields.String,
    # manu.CURR_STATE: fields.String,
    manu.ACTION: fields.String,
    manu.REFEREES: fields.String,
    "forceful_change": fields.String(
        required=False,
        default="",
        description="Only for Editor Move"
    )
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
        try:
            title = request.json.get(manu.TITLE)
            # curr_state = request.json.get(manu.CURR_STATE)
            action = request.json.get(manu.ACTION)
            referees = request.json.get(manu.REFEREES)
            print(referees)
            if isinstance(referees, str):
                referees = [referees]
            manuscript = manu.get_manuscript_by_title(title)
            if not manuscript:
                raise wz.NotFound(f"Manuscript '{title}' not found.")
            curr_state = manuscript[manu.STATE]
            extra_kwargs = {"manu": manuscript}
            if action == manu.EDITOR_MOVE:
                forceful_change = request.json.get("forceful_change", "")
                if not forceful_change:
                    raise wz.NotAcceptable("'forceful_change' required.")
                extra_kwargs["forceful_change"] = forceful_change
            if action == manu.ASSIGN_REF:
                if not referees:
                    raise wz.NotAcceptable("Must provide at least \
                    one referee to assign.")
                chosen_referee = random.choice(referees)
                # print("Chosen: ", chosen_referee)
                updated_state = manu.change_manuscript_state(
                    manuscript[manu.TITLE],
                    action, ref=chosen_referee, **extra_kwargs)
            # if len(referees) != 0:
            #     for ref in referees:
            #         updated_state = manu.change_manuscript_state(
            #           manuscript[manu.TITLE], action, ref=ref, **extra_kwargs
            #         )
            # else:
            else:
                updated_state = manu.change_manuscript_state(
                    manuscript[manu.TITLE],
                    action, ref=referees, **extra_kwargs)
            # manuscript[manu.STATE] = updated_state
            if "_id" in manuscript:
                del manuscript["_id"]
            # manu.update_manuscript(manuscript, manuscript)
        except Exception as err:
            raise wz.NotAcceptable(f"Bad action: {err}")
        return {
            "message": "Action received!",
            "title": title,
            "previous_state": curr_state,
            "updated_state": updated_state,
            "action": action,
            "referees": referees,
            "forceful_change": (
                "N/A" if action != manu.EDITOR_MOVE else forceful_change
            )
        }, HTTPStatus.OK


@api.route(f"{TEXT_EP}/<string:key>/")
class Text(Resource):
    def get(self, key):
        text = txt.read_one(key)
        if text is None:
            raise wz.NotAcceptable(f"No text found for key: {key}")
        return text


TEXT_CREATE_FLDS = api.model('AddNewTextEntry', {
    txt.KEY: fields.String,
    txt.TITLE: fields.String,
    txt.TEXT: fields.String,
})


@api.route(f'{TEXT_EP}/create')
class TextCreate(Resource):
    """
    Add a new text page to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(TEXT_CREATE_FLDS)
    def put(self):
        """
        Add a text.
        """
        try:
            key = request.json.get(txt.KEY)
            title = request.json.get(txt.TITLE)
            text = request.json.get(txt.TEXT)
            txt.create(key, title, text)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add text page: '
                                   f'{err=}')
        return {
            MESSAGE: 'Text page added!',
        }


@api.route(f"{TEXT_EP}/<string:key>/update")
class TextUpdate(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Text entry not found')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    def put(self, key):
        try:
            text_data = txt.read_one(key)
            if not text_data:
                raise wz.NotFound(f"No text found for key: {key}")

            title = request.json.get(txt.TITLE, text_data.get(txt.TITLE))
            text = request.json.get(txt.TEXT, text_data.get(txt.TEXT))

            if title is None and text is None:
                raise wz.NotAcceptable("No changes were submitted")

            txt.update(key, title, text)
        except wz.NotFound as err:
            return {"message": str(err)}, HTTPStatus.NOT_FOUND
        except Exception as err:
            return {"message": f"Could not update text: {err}"},
        HTTPStatus.NOT_ACCEPTABLE

        return {
            MESSAGE: 'Text updated successfully!',
            RETURN: txt.read_one(key)
        }, HTTPStatus.OK

def format_output(result):
    # Assuming result.stdout is in bytes, you may want to decode it to a string
    return result.stdout.decode('utf-8') if result.stdout else "No output"


@api.route(f"/servers/logs/error")
class ErrorLog(Resource):
    """
    See the most recent portions of error log
    """
    @api.response(HTTPStatus.OK.value, 'Success')
    def get(self):
        result = subprocess.run(f'tail {ELOG_LOC}', shell=True,
                                stdout=subprocess.PIPE)
        return {ELOG_KEY: format_output(result)}

