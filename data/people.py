"""
This module interfaces to our user data.
"""
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


def create_person(name: str, affiliation: str, email: str):
    """
    Our contract:
        - Takes in a new name, affiliation, and email
          to create a new person in the people dictionary
    """
    if email in TEST_PERSON_DICT:
        raise ValueError(f'This is a duplicate person{email=}')
    TEST_PERSON_DICT[email] = {
        NAME: name,
        AFFILIATION: affiliation,
        EMAIL: email}

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
