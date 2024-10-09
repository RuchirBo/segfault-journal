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

def update_users(name: str, affiliation: str, email: str):
    """
    Our contract:
        -TO BE UPDATED DEPENDING ON WHAT IS DONE IN CLASS
        - Updates a specific user's field in our dictionary
        - Takes in a user name and values to be updated
    """
    if email not in TEST_PERSON_DICT:
        raise ValueError(f'The email for the person you are trying to update does not exist {email=}')
    
    #TO BE UPDATED DEPENDING ON WHAT IS DONE IN CLASS
    TEST_PERSON_DICT[email] = {NAME: name, AFFILIATION: affiliation,
                          EMAIL: email}
    return
