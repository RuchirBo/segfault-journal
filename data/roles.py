

"""
This module manages person roles for a journal.
"""
from copy import deepcopy

AUTHOR_CODE = 'AU'
TEST_CODE = AUTHOR_CODE
ED_CODE = 'ED'
TEST_NEW_CODE = ED_CODE
ME_CODE = 'ME'
CE_CODE = 'CE'
RE_CODE = 'RE'

ROLES = {
    AUTHOR_CODE: 'Author',
    CE_CODE: 'Consulting Editor',
    ED_CODE: 'Editor',
    ME_CODE: 'Managing Editor',
    RE_CODE: 'Referee',
}

MH_ROLES = [CE_CODE, ED_CODE, ME_CODE]


def read() -> dict:
    return deepcopy(ROLES)


def get_roles() -> dict:
    return read()


def get_noncopy_roles() -> dict:
    return ROLES


def get_masthead_roles() -> dict:
    roles = get_roles()
    masthead_roles = {
        role: value
        for role, value in roles.items()
        if role in MH_ROLES
    }
    return masthead_roles


def is_valid(code: str) -> bool:
    return code in ROLES


def is_masthead_role(code: str) -> bool:
    return is_valid(code) and code in MH_ROLES


def get_role_codes() -> list:
    return list(ROLES.keys())


def delete_roles(_id):
    all_roles = get_noncopy_roles()
    if _id in all_roles:
        del all_roles[_id]
        return _id
    else:
        return None


def create_roles(code, name) -> dict:
    all_roles = get_noncopy_roles()
    if code in all_roles:
        return None
    else:
        all_roles[code] = name
        return all_roles


def update(code: str, name: str) -> dict:
    all_roles = get_noncopy_roles()
    if code in all_roles:
        all_roles[code] = name
        return all_roles
    else:
        return None


def main():
    print(get_roles())
    print(get_masthead_roles())


if __name__ == '__main__':
    main()
