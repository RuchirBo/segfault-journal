import data.people as ppl
import data.roles as roles

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
DOMAIN_UNDERSCORE = "i.like.underscores@but_they_are_not_allowed_here"
# Local-Part is longer than 64 characters
TOO_LONG_EMAIL = "1234567890123456789012345678901234567890123456789012345678901234+x@example.com"

# Valid Test Emails:
VALID_LONG = "long.email-address-with-hyphens@and.subdomains.example.com"
SLASH_CHAR = "name/surname@example.com"

# Valid Roles
VALID_ROLES = [roles.AUTHOR_CODE, 'ED']  # Author and Editor


# ADD_EMAIL = "john.smith@nyu.edu"
# def test_create_person():
#     ppl.create_person("John Smith", "NYU", ADD_EMAIL)
#     people = ppl.get_users()
#     assert ADD_EMAIL in people


ADD_EMAIL = "jon.smore@nyu.edu"
def test_create_person_with_roles():
    ppl.create_person("Jon Smore", "NYU", ADD_EMAIL, VALID_ROLES)
    people = ppl.get_users()
    assert ADD_EMAIL in people
    person_roles = people[ADD_EMAIL][ppl.ROLES]
    assert set(person_roles) == set(VALID_ROLES)


# def test_is_valid_email_at():
#     assert not ppl.is_valid_email(NO_AT)
#     assert not ppl.is_valid_email(DOUBLE_AT)


# def test_is_valid_no_name():
#     assert not ppl.is_valid_email(NO_NAME)


# def test_is_valid_no_domain():
#     assert not ppl.is_valid_email(NO_DOMAIN)


# def test_is_valid_dots():
#     assert not ppl.is_valid_email(DOUBLE_DOT)
#     assert not ppl.is_valid_email(FIRST_DOT)
#     assert not ppl.is_valid_email(LAST_DOT)


# def test_is_valid_hyphens():
#     assert not ppl.is_valid_email(FIRST_HYPHEN)
#     assert not ppl.is_valid_email(LAST_HYPHEN)


# def test_is_valid_domain_underscore():
#     assert not ppl.is_valid_email(DOMAIN_UNDERSCORE)


# def test_is_valid_length():
#     assert not ppl.is_valid_email(TOO_LONG_EMAIL)
#     assert ppl.is_valid_email(VALID_LONG)

# def test_is_valid_slash():
#     assert ppl.is_valid_email(SLASH_CHAR)


# def test_update():
#     people = ppl.read()
#     assert ADD_EMAIL in people
#     ppl.update_users("John Smith", ADD_EMAIL)
#     people = ppl.update_users()
    
# def test_delete_person():
#     people = ppl.read()
#     old_len = len(people)
#     ppl.delete(ppl.DEL_EMAIL)
#     people = ppl.read()
#     assert len(people) < old_len
#     assert ppl.DEL_EMAIL not in people