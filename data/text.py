"""
This module interfaces to our user data.
"""

# fields
KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

TEST_KEY = 'HomePage'
SUBM_KEY = 'SubmissionsPage'
DEL_KEY = 'DeletePage'

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
        TITLE: 'Home Page',
        TEXT: 'This is a text to delete.',
    },
}


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user email.
        - Each user email must be the key for another dictionary.
    """
    text = text_dict
    return text


def read_one(key: str) -> dict:
    # This should take a key and return the page dictionary
    # for that key. Return an empty dictionary if key not found.
    result = {}
    if key in text_dict:
        result = text_dict[key]
    return result


def create(title: str, text: str, key: str):
    """
    Our contract:
       - Adds a new entry to the text_dict
       - The entry includes a title and text
    """
    if key in text_dict:
        raise ValueError(f'This is a duplicate{key=}')
    text_dict[key] = {
        TITLE: title,
        TEXT: text,
    }
    return key


def delete(_id):
    """
    Our contract:
        - Deletes an entry from text_dict
    """
    text = read()
    if _id in text:
        del text[_id]
        return _id
    else:
        return None


def update(key: str, title: str = None, text: str = None):
    """
    Our contract:
        - Updates the title or text of an entry in text_dict
        - Only updates if the key is in the text_dict
    """
    if key not in text_dict:
        raise ValueError(
            f"Key '{key}' not found in text_dict."
        )
    if title is not None:
        text_dict[key][TITLE] = title
    if text is not None:
        text_dict[key][TEXT] = text
    return key


def main():
    print(read())


if __name__ == '__main__':
    main()
