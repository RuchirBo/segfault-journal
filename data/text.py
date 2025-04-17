"""
This module interfaces to our user data.
"""

import data.db_connect as dbc

TEXT_COLLECT = "text"

# fields
KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

TEST_KEY = 'HomePage'
TEST_TITLE = "Home Page"
TEST_TEXT = "This is a journal about building API servers."

SUBM_KEY = 'SubmissionsPage'
DEL_KEY = 'DeletePage'
UPD_KEY = 'UpdatePage'

TEST_UPD_VAL = 'Test update value'

text_dict = {
    TEST_KEY: {
        TITLE: 'Home Page',
        TEXT: 'This is a journal about building API servers.',
    },
    SUBM_KEY: {
        TITLE: "Submissions Page",
        TEXT: "All submissions must be original work in Word format"
    },
    DEL_KEY: {
        TITLE: 'Delete Page',
        TEXT: 'This is a text to delete.',
    },
    UPD_KEY: {
        TITLE: 'Update Page',
        TEXT: 'This is a text to update.',
    }
}

client = dbc.connect_db()


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = dbc.read_dict(TEXT_COLLECT, KEY)
    return text


def read_one(key: str) -> dict:
    # This should take a key and return the page dictionary
    # for that key. Returns None if key not found.
    doc = dbc.fetch_one(TEXT_COLLECT, {KEY: key})
    if doc is not None:
        return doc
    return text_dict.get(key)


def create(title: str, text: str, key: str):
    """
    Our contract:
       - Adds a new entry to the text_dict
       - The entry includes a title and text
    """
    if (exists(key)):
        raise ValueError(f'This is a duplicate{key=}')
    text = {
        KEY: key,
        TITLE: title,
        TEXT: text,
    }
    dbc.create(TEXT_COLLECT, text)
    return key


def delete(key: str):
    """
    Our contract:
        - Deletes an entry from text_dict
    """
    result = dbc.delete(TEXT_COLLECT, {KEY: key})
    if result is None:
        raise ValueError(f"No key found with {key=}")


def update(key: str, title: str = None, text: str = None):
    """
    Our contract:
        - Updates the title or text of an entry in text_dict
        - Only updates if the key is in the text_dict
    """
    if not exists(key):
        raise ValueError(
            f"Key '{key}' not found in collection"
        )
    dbc.update(
        TEXT_COLLECT,
        {KEY: key},
        {
            "$set": {
                TITLE: title,
                TEXT: text
            }
        },
    )


def exists(key: str):
    return read_one(key) is not None


def main():
    print(read())


if __name__ == '__main__':
    main()
