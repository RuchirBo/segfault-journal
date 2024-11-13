import data.roles as rls
from unittest import mock
ADD_ROLE = "NR"
SAMPLE_ROLES = rls.get_roles()
SAMPLE_ROLES['patched'] = 'yes'


def test_get_masthead_roles():
    mh_roles = rls.get_masthead_roles()
    assert isinstance(mh_roles, dict)


def test_get_role_codes():
    codes = rls.get_role_codes()
    assert isinstance(codes, list)
    for code in codes:
        assert isinstance(code, str)


def test_patching():
    actual_codes = rls.get_role_codes()
    with mock.patch.dict('data.roles.ROLES', SAMPLE_ROLES, clear=True):
        codes = rls.get_role_codes()
        assert "patched" in codes
        assert "patched" not in actual_codes


def test_create_roles():
    with mock.patch.dict('data.roles.ROLES', SAMPLE_ROLES, clear=True):
        rls.create_roles(ADD_ROLE, "New Role")
        codes = rls.get_role_codes()
        assert ADD_ROLE in codes


def test_delete_roles():
    with mock.patch.dict('data.roles.ROLES', SAMPLE_ROLES, clear=True):
        rls.create_roles(ADD_ROLE, "New Role")
        codes = rls.get_role_codes()
        assert ADD_ROLE in codes
        rls.delete_roles(ADD_ROLE)
        del_codes = rls.get_role_codes()
        assert ADD_ROLE not in del_codes
        assert rls.delete_roles("NOTAROLE") == None