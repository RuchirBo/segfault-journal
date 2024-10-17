import data.text as tx

def test_read():
    text_data = tx.read()
    assert isinstance(text_data, dict)
    assert len(text_data) > 0
    for _id, text in text_data.items():
        assert isinstance(_id, str)
        assert tx.TITLE in text
        assert tx.TEXT in text


def test_read_one():
    text_data = tx.read_one(tx.TEST_KEY)
    assert isinstance(text_data, dict)
    assert len(text_data) > 0


def test_read_one_parameters():
    text_data = tx.read_one(tx.TEST_KEY)
    assert tx.TITLE in text_data
    assert tx.TEXT in text_data


def test_read_one_invalid():
    text_data = tx.read_one("")
    assert text_data == {}

