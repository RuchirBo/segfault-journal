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
