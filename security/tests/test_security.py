import security.security as security

def test_read():
    records = security.read()
    assert isinstance(records, dict)
    for feature in records:
        assert isinstance(feature, str)
        assert len(feature) > 0