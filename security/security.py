import data.db_connect as db_connect

COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'

PEOPLE = 'people'


security_records = {
     PEOPLE: {
         CREATE: {
             USER_LIST: ['ejc369@nyu.edu'],
             CHECKS: {
                 LOGIN: True,
             },
         },
     },
 }


def read() -> dict:
    # dbc.read()
    return security_records

def delete_acc(email: str):
    query = {'type': PEOPLE, 'email': email}
    db_connect.connect_db()
    return db_connect.delete_one(COLLECT_NAME, query)