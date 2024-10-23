"""
This module interfaces to our user data.
"""

import re
from data import roles  # importing functions from roles.py

MIN_USER_NAME_LEN = 2
# fields
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

TEST_EMAIL = 'ejc369@nyu.edu'

TEST_PERSON_DICT = {
    TEST_EMAIL: {
        NAME: 'Euguene Callahan',
        ROLES: [],
        AFFILIATION: 'NYU',
        EMAIL: TEST_EMAIL
    }
}


CHAR_OR_DIGIT = '[A-Za-z0-9]'


def is_valid_email(email: str) -> bool:
    return re.match(f"{CHAR_OR_DIGIT}.*@{CHAR_OR_DIGIT}.*", email)


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
    """
    ppl = TEST_PERSON_DICT
    return ppl


def update_users(newName: str, affiliation: None, email: str):
    """
    Our contract:
        -Name can't be blank
        -Email can't be changed
        -Affiliation can be blank
    """
    if email in TEST_PERSON_DICT:
        TEST_PERSON_DICT[email] = {
            NAME: newName,
            AFFILIATION: affiliation,
            EMAIL: email}
        return email
    else:
        raise ValueError(
            f'The email for the person you are trying '
            f'to update does not exist {email=}'
        )


def create_person(name: str, affiliation: str, email: str, 
                  roles_list: list = None):
    """
    Our contract:
        - Takes in a new name, affiliation, email, and role(s)
          to create a new person in the people dictionary
    """
    if email in TEST_PERSON_DICT:
        raise ValueError(f'This is a duplicate person{email=}')
    valid_roles = []
    if roles_list:
        for role in roles_list:
            if roles.is_valid(role):
                valid_roles.append(role)
            else:
                raise ValueError(f'Invalid role: {role}')
    TEST_PERSON_DICT[email] = {
        NAME: name,
        AFFILIATION: affiliation,
        EMAIL: email,
        ROLES: valid_roles}

    return email


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    people = TEST_PERSON_DICT
    return people


def delete_person(_id):
    """
    Our contract:
        - Deleted a person in the people dictionary based on provided ID
    """
    people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None
