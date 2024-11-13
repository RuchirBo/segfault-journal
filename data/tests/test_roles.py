import data.roles as rls
ADD_ROLE = "RE"

def test_get_masthead_roles():
    mh_roles = rls.get_masthead_roles()
    assert isinstance(mh_roles, dict)


def test_get_role_codes():
    codes = rls.get_role_codes()
    assert isinstance(codes, list)
    for code in codes:
        assert isinstance(code, str)


def test_create_roles():
    rls.create_roles(ADD_ROLE, "Referee")
    codes = rls.get_role_codes()
    assert ADD_ROLE in codes
