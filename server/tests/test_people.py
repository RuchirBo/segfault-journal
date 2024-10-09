import data.people as ppl

ADD_EMAIL = "john.smith@nyu.edu"
def test_create_person():
    ppl.create_person("John Smith", "NYU", ADD_EMAIL)
    people = ppl.get_users()
    assert ADD_EMAIL in people