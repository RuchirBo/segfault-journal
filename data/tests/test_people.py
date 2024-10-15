import data.people as ppl

ADD_EMAIL = "john.smith@nyu.edu"
def test_create_person():
    ppl.create_person("John Smith", "NYU", ADD_EMAIL)
    people = ppl.get_users()
    assert ADD_EMAIL in people

# def test_get_people():
#     people = ppl.get_people()
#     assert isinstance(people)
#     assert len(people) > 0
#     #check for string ID's
#     for _id, person in people.items():
#         assert isinstance(_id, str)
#         assert ppl.NAME in person

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