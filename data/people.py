"""
This module interfaces to our user data.
"""

import re
import data.roles as rls  # importing functions from roles.py

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

MH_FIELDS = [NAME, AFFILIATION]

pattern = (
    r'^[A-Za-z0-9\-\/_](?!.*\.\.)[A-Za-z0-9\-\/_\.]{0,63}@[A-Za-z0-9\-]+'
    r'(\.[A-Za-z0-9\-]+)+$'
)


def is_valid_email(email: str) -> bool:
    return re.match(pattern, email)


def is_valid_person(name: str, affiliation: str,
                    email: str,
                    roles_list: list = []) -> None:
    ppl = TEST_PERSON_DICT
    if email in ppl:
        raise ValueError(f'Adding duplicate {email=}')
    if not is_valid_email(email):
        raise ValueError(f'Invalid email {email}')
    elif roles_list:
        for role in roles_list:
            if not rls.is_valid(role):
                raise ValueError(f'Invalid role: {role}')


def read() -> dict:
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    people = TEST_PERSON_DICT
    return people


def read_one(email: str) -> dict:
    """
    Return a person record if email present in DB,
    else None.
    """
    return TEST_PERSON_DICT.get(email)


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
    """
    ppl = TEST_PERSON_DICT
    return ppl


def update_users(newName: str, affiliation: None,
                 email: str, roles_list: list = None):
    """
    Our contract:
        -Name can't be blank
        -Email can't be changed
        -Affiliation can be blank
    """
    is_valid_person(newName, affiliation, email, roles_list)
    TEST_PERSON_DICT[email] = {
        NAME: newName,
        AFFILIATION: affiliation,
        EMAIL: email,
        ROLES: roles_list}


def create_person(name: str, affiliation: str, email: str,
                  role: str = None):
    """
    Our contract:
        - Takes in a new name, affiliation, email, and role(s)
          to create a new person in the people dictionary
    """

    is_valid_person(name, affiliation, email, [role])
    valid_roles = []
    if role:
        valid_roles.append(role)
        TEST_PERSON_DICT[email] = {
            NAME: name,
            AFFILIATION: affiliation,
            EMAIL: email,
            ROLES: valid_roles}
    return email


# def read():
#     """
#     Our contract:
#         - No arguments.
#         - Returns a dictionary of users keyed on user email.
#         - Each user email must be the key for another dictionary.
#     """
#     people = TEST_PERSON_DICT
#     return people


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


def has_role(person, role) -> bool:
    if role in person.get(ROLES):
        return True
    return False


def has_masthead_role(person) -> bool:
    print("ROLES", person.get(ROLES))
    for role in person.get(ROLES):
        if rls.is_masthead_role(role):
            return True
    return False


def create_mh_rec(person: dict) -> dict:
    mh_rec = {}
    for field in MH_FIELDS:
        mh_rec[field] = person.get(field, '')
    return mh_rec


def get_masthead() -> dict:
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_w_role = []
        people = read()
        for _id, person in people.items():
            if has_role(person, mh_role):
                pass
                # rec = create_mh_rec(person)
                # people_w_role.append(rec)
        masthead[text] = people_w_role
    return masthead


def add_role_to_person(email: str, role: str) -> None:
    if not rls.is_valid(role):
        raise ValueError(f"Invalid Role: {role}")
    person = read_one(email)
    if person:
        if role not in person[ROLES]:
            person[ROLES].append(role)
    else:
        raise ValueError(f"No person for this email: {email}")


def get_person_roles(email: str) -> list:
    person = read_one(email)
    return person.get(ROLES, []) if person else []


def main():
    print(get_masthead())


if __name__ == '__main__':
    main()
