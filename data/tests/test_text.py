import data.text as tx

ADD_KEY = "john.smith@nyu.edu"
ADD_TITLE = "Journal Entry"
ADD_TEXT = "This is my new journal entry."

def test_create():
    print(tx.read())
    tx.create(tx.TEST_TITLE, tx.TEST_TEXT, tx.TEST_KEY)
    print(tx.read())
    print(tx.exists(tx.TEST_KEY))
    assert tx.exists(tx.TEST_KEY)

def test_read():
    text_data = tx.read()
    print(text_data)
    assert isinstance(text_data, dict)
    assert len(text_data) > 0
    for key, text in text_data.items():
        assert isinstance(key, str)
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
    assert text_data == None


def test_update():
    assert tx.exists(tx.TEST_KEY)
    tx.update(tx.TEST_KEY, ADD_TITLE, ADD_TEXT)
    upEntry = tx.read_one(tx.TEST_KEY)
    assert upEntry[tx.TITLE] == ADD_TITLE
    assert upEntry[tx.TEXT] == ADD_TEXT


def test_delete():
    text = tx.read()
    old_len = len(text)
    tx.delete(tx.TEST_KEY)
    text = tx.read()
    assert len(text) < old_len
    assert tx.TEST_KEY not in text
