"""
This module interfaces to our user data.
"""

import re
import data.roles as rls  # importing functions from roles.py
import data.db_connect as dbc

PEOPLE_COLLECT = 'people'

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

client = dbc.connect_db()
print(f'{client=}')


def is_valid_email(email: str) -> bool:
    return re.match(pattern, email)


def is_valid_person(name: str, affiliation: str,
                    email: str,
                    roles_list: list = []) -> bool:
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    if roles_list:
        for role in roles_list:
            if not rls.is_valid(role):
                raise ValueError(f'Invalid role: {role}')
    return True


def read() -> dict:
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    people = dbc.read_dict(PEOPLE_COLLECT, EMAIL)
    print(f'{people=}')
    return people


def read_one(email: str) -> dict:
    """
    Return a person record if email present in DB by email.
    """
    return dbc.fetch_one(PEOPLE_COLLECT, {EMAIL: email})


def get_users():
    """
    Note: I am not sure if this fx is being used /is needed
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
    """
    ppl = TEST_PERSON_DICT
    return ppl


def update_users(new_name: str, affiliation: str,
                 email: str, roles_list: list):
    """
    Our contract:
        -Name can't be blank
        -Email can't be changed
        -Affiliation can be blank
    """
    if not exists(email):
        raise ValueError(f'Updating non-existent person: {email=}')
    dbc.update(
        PEOPLE_COLLECT,
        {EMAIL: email},
        {
            "$set": {
                NAME: new_name,
                AFFILIATION: affiliation,
                ROLES: roles_list,
            }
        },
    )


def create_person(name: str, affiliation: str, email: str,
                  roles: list = []):
    """
    Our contract:
        - Takes in a new name, affiliation, email, and role(s)
          to create a new person in the people dictionary
    """
    if exists(email):
        raise ValueError(f'Adding duplicate {email=}')
    is_valid_person(name, affiliation, email, roles)
    person = {
        NAME: name,
        AFFILIATION: affiliation,
        EMAIL: email,
        ROLES: roles,
    }
    dbc.create(PEOPLE_COLLECT, person)
    return email


def delete_person(email: str):
    """
    Our contract:
        - Deleted a person in the people dictionary based on provided ID
    """
    result = dbc.delete(PEOPLE_COLLECT, {EMAIL: email})
    if result is None:
        raise ValueError(f"No person found with {email=}")


def has_role(person: dict, role: str) -> bool:
    return role in person.get(ROLES, [])


def has_masthead_role(person) -> bool:
    print("ROLES", person.get(ROLES))
    for role in person.get(ROLES):
        if rls.is_masthead_role(role):
            return True
    return False


def create_mh_rec(person: dict) -> dict:
    """
    Creates a masthead record for a person.
    """
    mh_rec = {}
    for field in MH_FIELDS:
        mh_rec[field] = person.get(field, '')
    return mh_rec


def get_masthead() -> dict:
    """
    Retrieves the masthead by roles from MongoDB.
    """
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_with_role = []
        people = dbc.read(PEOPLE_COLLECT)
        for person in people:
            if has_role(person, mh_role):
                rec = create_mh_rec(person)
                people_with_role.append(rec)
        masthead[text] = people_with_role
    return masthead


def add_role_to_person(email: str, role: str) -> None:
    if not rls.is_valid(role):
        raise ValueError(f"Invalid Role: {role}")
    person = read_one(email)
    if not person:
        raise ValueError(f"No person found with {email=}")
    if role not in person.get(ROLES, []):
        dbc.update(
            PEOPLE_COLLECT,
            {EMAIL: email},
            {"$addToSet": {ROLES: role}},
        )
    else:
        raise ValueError(f"Role {role} already exists for {email}")


def exists(email: str) -> bool:
    return read_one(email) is not None


def get_person_roles(email: str) -> list:
    person = read_one(email)
    return person.get(ROLES, []) if person else []


def delete_role_from_person(email: str, role: str) -> None:
    if not rls.is_valid(role):
        raise ValueError(f"Invalid Role: {role}")
    person = read_one(email)
    if not person:
        raise ValueError(f"No person found with {email=}")
    if role in person.get(ROLES, []):
        dbc.update(
            PEOPLE_COLLECT,
            {EMAIL: email},
            {"$pull": {ROLES: role}},
        )
    else:
        raise ValueError(f"Role {role} does not exist for {email}")


def get_people_by_role(role):
    all_people = read()
    return [
        person for person in all_people.values()
        if isinstance(person, dict) and role in person.get("roles", [])
    ]


def main():
    print(get_masthead())


if __name__ == '__main__':
    main()
