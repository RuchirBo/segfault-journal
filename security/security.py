import data.db_connect as db_connect

COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'
LOGIN_KEY = 'login_key'
IP_ADDR = 'ip_address'
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

def is_valid_key(user_id: str, login_key: str):
    """
    This is just a mock of the real is_valid_key() we'll write later.
    """
    return True


def check_login(user_id: str, **kwargs):
    if LOGIN_KEY not in kwargs:
        return False
    return is_valid_key(user_id, kwargs[LOGIN_KEY])


def check_ip(user_id: str, **kwargs):
    if IP_ADDR not in kwargs:
        return False
    # we would check user's IP address here
    return True