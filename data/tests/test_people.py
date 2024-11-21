import pytest
import data.people as ppl
import data.roles as roles
from unittest.mock import patch

from data.roles import TEST_CODE as TEST_ROLE_CODE
from data.roles import TEST_NEW_CODE as TEST_NEW_ROLE_CODE
from data.roles import ED_CODE as TEST_ED_CODE

# Invalid Test Emails:
NO_AT = 'jkajsd'
DOUBLE_AT = "a@b@c@example.com"
NO_NAME = '@kalsj'
NO_DOMAIN = 'kajshd@'
DOUBLE_DOT = "johnny..appleseed@forest.gov"
FIRST_DOT = ".me@myemail"
LAST_DOT = "me.@myemail"
FIRST_HYPHEN = "me@-myemail"
LAST_HYPHEN = "me@myemail-"
INVALID_CHAR = "me!@myemail"
INVALID_DOMAIN_UNDERSCORE = "i.like.underscores@but_they_are_not_allowed_here"
VALID_UNDERSCORE = "temp_person@example.org"
# Local-Part is longer than 64 characters
TOO_LONG_EMAIL = '12345678901234567890123456789012345678901'\
    + '23456789012345678901234+x@example.com'


# Valid Test Emails:
VALID_LONG = "long.email-address-with-hyphens@and.subdomains.example.com"
SLASH_CHAR = "name/surname@example.com"
VALID_EMAIL = "john.smith@nyu.edu"

# Valid Roles
VALID_ROLES = [roles.AUTHOR_CODE, 'ED']  # Author and Editor
INVALID_ROLE = "INVALID"


ADD_EMAIL = "john.smith@nyu.edu"
NEW_EMAIL = "new_email@nyu.edu"

TEMP_EMAIL = 'tempperson@temp.org'
TEMP_EMAIL2 = 'temp2person@temp.org'
TEMP_EMAIL3 = 'temp3person@temp.org'
TEMP_EMAIL4 = 'temp4person@temp.org'
BOB_EMAIL = 'bob.ross@nyu.edu'


def test_create_person():
    if ppl.read_one(ADD_EMAIL):
        ppl.delete_person(ADD_EMAIL)

    ppl.create_person("John Smith", "NYU", ADD_EMAIL, 'AU')
    people = ppl.get_users()
    assert ADD_EMAIL in people

    ppl.delete_person(ADD_EMAIL)


def test_delete_person():
    people = ppl.read()
    old_len = len(people)
    ppl.delete_person(ADD_EMAIL)
    people = ppl.read()
    assert len(people) < old_len
    assert ADD_EMAIL not in people

def test_update_person_role():
    ppl.create_person('Joe Smith', 'NYU', TEMP_EMAIL4, TEST_ROLE_CODE)
    ppl.update_person_role('Joe Smith', 'NYU', TEMP_EMAIL4, TEST_ROLE_CODE, TEST_NEW_ROLE_CODE)
    person_roles = ppl.get_person_roles(TEMP_EMAIL4)
    assert not TEST_ROLE_CODE in person_roles
    assert TEST_NEW_ROLE_CODE in person_roles 

# def test_create_person_with_roles():
#    ppl.create_person("Jon Smore", "NYU", ADD_EMAIL, VALID_ROLES)
#    people = ppl.get_users()
#    assert ADD_EMAIL in people
#    person_roles = people[ADD_EMAIL][ppl.ROLES]
#    assert set(person_roles) == set(VALID_ROLES)


def test_is_valid_email():
    assert ppl.is_valid_email(VALID_EMAIL)


def test_is_valid_email_at():
    assert not ppl.is_valid_email(NO_AT)
    assert not ppl.is_valid_email(DOUBLE_AT)


def test_is_valid_no_name():
    assert not ppl.is_valid_email(NO_NAME)


def test_is_valid_no_domain():
    assert not ppl.is_valid_email(NO_DOMAIN)


def test_is_valid_dots():
    assert not ppl.is_valid_email(DOUBLE_DOT)
    assert not ppl.is_valid_email(FIRST_DOT)
    assert not ppl.is_valid_email(LAST_DOT)


def test_is_valid_hyphens():
    assert not ppl.is_valid_email(FIRST_HYPHEN)
    assert not ppl.is_valid_email(LAST_HYPHEN)


def test_is_invalid_domain_underscore():
    assert not ppl.is_valid_email(INVALID_DOMAIN_UNDERSCORE)


def test_is_valid_domain_underscore():
    assert ppl.is_valid_email(VALID_UNDERSCORE)


def test_is_valid_length():
    assert not ppl.is_valid_email(TOO_LONG_EMAIL)
    assert ppl.is_valid_email(VALID_LONG)


def test_is_valid_slash():
    assert ppl.is_valid_email(SLASH_CHAR)


def test_is_valid_char():
    assert not ppl.is_valid_email(INVALID_CHAR)


@pytest.fixture(scope='function')
def temp_person():
    ret = ppl.create_person('Joe Smith', 'NYU', TEMP_EMAIL, TEST_ROLE_CODE)
    yield ret
    ppl.delete_person(ret)


def test_has_role(temp_person):
    person_rec = ppl.read_one(temp_person)
    assert ppl.has_role(person_rec, TEST_ROLE_CODE)


@patch('data.people.get_masthead', autospec=True,
       return_value={'NAME': 'Joe Smith'})
def test_get_masthead(mock_read):
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)


@pytest.fixture(scope='function')
def ed_person():
    ret = ppl.create_person('Jane Smith', 'NYU', TEMP_EMAIL2, TEST_ED_CODE)
    yield ret
    ppl.delete_person(ret)


def test_create_masthead(ed_person):
    person_rec = ppl.read_one(ed_person)
    mh_rec = ppl.create_mh_rec(person_rec)
    assert isinstance(mh_rec, dict)
    for field in ppl.MH_FIELDS:
        assert field in mh_rec


def test_has_masthead_role(temp_person, ed_person):
    editor = ppl.read_one(ed_person)
    normal = ppl.read_one(temp_person)
    assert ppl.has_masthead_role(editor)
    assert not ppl.has_masthead_role(normal)


def test_is_valid_person():
    ppl.is_valid_person(
        'Bob Ross',
        'NYU',
        BOB_EMAIL,
        [TEST_ED_CODE])


def test_is_invalid_role_person():
    with pytest.raises(ValueError, match='Invalid role'):
        ppl.is_valid_person('Joe Smith', 'NYU', TEMP_EMAIL3, ['SOMETHING'])


def test_add_role_to_person(temp_person):
    new_role = roles.AUTHOR_CODE
    ppl.add_role_to_person(TEMP_EMAIL, new_role)
    person_roles = ppl.get_person_roles(TEMP_EMAIL)
    assert new_role in person_roles


def test_add_role_to_person_invalid_role(temp_person):
    with pytest.raises(ValueError, match="Invalid Role"):
        ppl.add_role_to_person(TEMP_EMAIL, INVALID_ROLE)


@pytest.fixture(scope='function')
def temp2_person():
    "Another fixture test to test specficially adding another role"
    ret = ppl.create_person('Joe Smith', 'NYU', TEMP_EMAIL, roles.AUTHOR_CODE)
    ppl.add_role_to_person(TEMP_EMAIL, roles.ED_CODE)
    yield ret
    ppl.delete_person(ret)


def test_get_person_roles(temp2_person):
    roles = ppl.get_person_roles(TEMP_EMAIL)
    assert roles == VALID_ROLES


@pytest.mark.skip(
        "Skipping this test because we can't access"
        " user's information other than email"
)
def test_update(temp_person):
    ppl.update_users(
        "John Smith",
        "test affiliation",
        temp_person,
        temp_person
    )


def test_invalid_update():
    with pytest.raises(
        ValueError, match=rf"User not found with email='{NEW_EMAIL}'"
    ):
        ppl.update_users(
            "Janet Jackson",
            "test affiliation",
            NEW_EMAIL,
            roles.ED_CODE
        )


def test_delete_role_from_person(temp_person):
    role = roles.AUTHOR_CODE
    ppl.add_role_to_person(TEMP_EMAIL, role)
    person_roles = ppl.get_person_roles(TEMP_EMAIL)
    assert role in person_roles

    ppl.delete_role_from_person(TEMP_EMAIL, role)
    person_roles = ppl.get_person_roles(TEMP_EMAIL)
    assert not role in person_roles


def test_update_not_there(temp_person):
    with pytest.raises(ValueError):
        ppl.update('Will Fail', 'University of the Void',
                   'Non-existent email', VALID_ROLES)


def test_exists(temp_person):
    assert ppl.exists(temp_person)
