import security.security as security

def test_read():
    records = security.read()
    assert isinstance(records, dict)
    for feature in records:
        assert isinstance(feature, str)
        assert len(feature) > 0

def test_check_login_good():
    assert security.check_login(security.GOOD_USER_ID,
                           login_key='test_key')


def test_check_login_bad():
    assert not security.check_login(security.GOOD_USER_ID)