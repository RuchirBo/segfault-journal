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
    
    return

def update_users(newName: str, affiliation: None, email: str):
    """
    Our contract:
        -Name can't be blank
        -Email can't be changed
        -Affiliation can be blank
    """
    if email not in TEST_PERSON_DICT:
        raise ValueError(f'The email for the person you are trying to update does not exist {email=}')

    TEST_PERSON_DICT[email] = {NAME: newName, AFFILIATION: affiliation, EMAIL: email}
    return email

def create_person(name: str, affiliation: str, email: str):
    """
    Our contract:
        - Takes in a new name, affiliation, and email to create a new person in the people dictionary
    """
    if email in TEST_PERSON_DICT:
        raise ValueError(f'This is a duplicate person{email=}')
    TEST_PERSON_DICT[email] = {NAME: name, AFFILIATION: affiliation, EMAIL: email}