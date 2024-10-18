import data.text as tx

ADD_KEY = "john.smith@nyu.edu"
ADD_TITLE = "Journal Entry"
ADD_TEXT = "This is my new journal entry."

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


def test_create():
    key = tx.create(ADD_TITLE, ADD_TEXT, ADD_KEY)
    text_data = tx.read()
    assert key in text_data
    assert text_data[key]['title'] == ADD_TITLE
    assert text_data[key]['text'] == ADD_TEXT

def test_delete():
    text = tx.read()
    old_len = len(text)
    tx.delete(tx.DEL_KEY)
    text = tx.read()
    assert len(text) < old_len
    assert tx.DEL_KEY not in text

def test_create():
    new_title = "Journal Entry Update"
    new_text = "This is my updated journal entry."
    tx.update(tx.TEST_KEY, title=new_title, text=new_text)
    updated_entry = tx.read_one(tx.TEST_KEY)
    assert updated_entry[tx.TITLE] == new_title
    assert updated_entry[tx.TEXT] == new_text