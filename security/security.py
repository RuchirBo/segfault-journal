COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'

PEOPLE = 'people'

security_records = {}

temp_records = {
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
     global security_records
     # dbc.read()
     security_recs = temp_records
     return security_records




