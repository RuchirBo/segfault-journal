import data.people as ppl

# Invalid Test Emails:
NO_AT = 'jkajsd'
NO_NAME = '@kalsj'
NO_DOMAIN = 'kajshd@'
DOUBLE_DOT = "johnny..appleseed@forest.gov"
FIRST_DOT = ".me@myemail"
LAST_DOT = "me.@myemail"
FIRST_HYPHEN = "me@-myemail"
LAST_HYPHEN = "me@myemail-"
DOUBLE_AT = "a@b@c@example.com"
DOMAIN_UNDERSCORE = "i.like.underscores@but_they_are_not_allowed_here"
# Local-Part is longer than 64 characters
TOO_LONG_EMAIL = "1234567890123456789012345678901234567890123456789012345678901234+x@example.com"

# Valid Test Emails:
VALID_LONG = "long.email-address-with-hyphens@and.subdomains.example.com"
SLASH_CHAR = "name/surname@example.com"




ADD_EMAIL = "john.smith@nyu.edu"
def test_create_person():
    ppl.create_person("John Smith", "NYU", ADD_EMAIL)
    people = ppl.get_users()
    assert ADD_EMAIL in people

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