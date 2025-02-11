TITLE = 'title'
DISP_NAME = 'disp_name'
AUTHOR = 'author'
REFEREES = 'referees'

TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'

TEST_FLD_DISP_AUTHOR = 'Person'
TEST_FLD_DISP_REFEREE = 'Referee'


FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
    AUTHOR: {
        DISP_NAME: TEST_FLD_DISP_AUTHOR,
    },
    # REFEREES: {
    #     DISP_NAME: TEST_FLD_DISP_REFEREE,
    # },
}

import data.db_connect as dbc

MANU_COLLECT = 'manuscripts'

SUBMITTED = 'SUB'
IN_REF_REV = 'REV'
COPY_EDIT = 'CED'
AUTHOR_REVIEW = 'AUREVIEW'
FORMATTING = 'FORM'
PUBLISHED = 'PUB'
REJECTED = 'REJ'
WITHDRAW = 'WITHDRAW'

ACTION = "action"
CURR_STATE = "current_state"

AUTHOR_REVISIONS = 'AUTHREVISION'
EDITOR_REVIEW = 'EDREV'
WITHDRAWN = 'WITH'

TEST_STATE = SUBMITTED

VALID_STATES = [
    SUBMITTED,
    IN_REF_REV,
    COPY_EDIT,
    AUTHOR_REVIEW,
    FORMATTING,
    PUBLISHED,
    REJECTED,
    AUTHOR_REVISIONS,
    EDITOR_REVIEW,
    WITHDRAWN,
]

SAMPLE_MANU = {
    TITLE: 'Test Title',
    AUTHOR: 'Test Person',
    REFEREES: [],
}

client = dbc.connect_db()
print(f'{client=}')


def get_states() -> list:
    return VALID_STATES
def is_valid_state(state: str) -> bool:
    return state in VALID_STATES


ACCEPT = 'ACC'
ACCEPT_WITH_REV = 'ACCWITHREV'
SUBMIT_REV = 'SUBREV'
ASSIGN_REF = 'ARF'
DONE = 'DON'
REJECT = 'REJ'
DELETE_REF = 'DRF'
TEST_ACTION = ACCEPT

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DONE,
    REJECT,
    WITHDRAW,
    ACCEPT_WITH_REV,
    SUBMIT_REV,
    DELETE_REF
]

def get_actions() -> list:
    return VALID_ACTIONS

def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS

def assign_ref(manu: dict, ref: str, extra=None) -> str:
    print(extra)
    manu[REFEREES].append(ref)
    return IN_REF_REV

def delete_ref(manu: dict, ref: str) -> str:
    if len(manu[REFEREES]) > 0:
        manu[REFEREES].remove(ref)
    if len(manu[REFEREES]) > 0:
        return IN_REF_REV
    else:
        return SUBMITTED

FUNC = 'FUNC'

COMMON_ACTIONS = {
    WITHDRAW: {
        FUNC: lambda **kwargs: WITHDRAWN,
    },
}

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        **COMMON_ACTIONS,
    },
    IN_REF_REV: {
        ACCEPT: {
            'FUNC': lambda **kwargs: COPY_EDIT,
        },
        ACCEPT_WITH_REV: {
            'FUNC': lambda **kwargs: AUTHOR_REVISIONS,
        },
        ASSIGN_REF: {
            FUNC: assign_ref,
        },
        SUBMIT_REV: {
            'FUNC': lambda **kwargs: IN_REF_REV,
        },
        DELETE_REF: {
            FUNC: delete_ref,
        },
        REJECT: {
            FUNC: lambda **kwargs: REJECTED,
        },
        **COMMON_ACTIONS,
    },
    COPY_EDIT: {
        DONE: {
            FUNC: lambda **kwargs: AUTHOR_REVIEW,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVIEW: {
        DONE: {
            'FUNC': lambda **kwargs: FORMATTING,
        },
        **COMMON_ACTIONS,
    },
    FORMATTING: {
        DONE: {
            'FUNC': lambda **kwargs: FORMATTING,
        },
        **COMMON_ACTIONS,
    },
    AUTHOR_REVISIONS: {
        DONE: {
            'FUNC': lambda **kwargs: EDITOR_REVIEW,
        },
        **COMMON_ACTIONS,
    },
    EDITOR_REVIEW: {
        ACCEPT: {
            'FUNC': lambda **kwargs: COPY_EDIT,
        },
        **COMMON_ACTIONS,
    },
    PUBLISHED: {},
    REJECTED:{},
    WITHDRAWN:{}
}



def handle_action(curr_state, action, **kwargs) -> str:
    if not is_valid_state(curr_state):
        raise ValueError(f'Invalid state: {curr_state}')
    if not is_valid_action(action):
        raise ValueError(f'Invalid action: {action}')
    if curr_state not in STATE_TABLE or action not in STATE_TABLE[curr_state]:
        raise ValueError(f'Invalid action {action} for state {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](**kwargs)


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions

def create_manuscript(manuscript: dict):
    all_fields = [TITLE, AUTHOR, REFEREES]
    for key in all_fields:
        if key not in manuscript:
            raise ValueError(f"Missing required field for manuscript: {key}")
    dbc.create(MANU_COLLECT, manuscript)
    return f"Manuscript created successfully."


def update_manuscript(old_manuscript: dict, new_manuscript: dict):
    old_manu = dbc.fetch_one(collection = MANU_COLLECT, filt={
        TITLE: old_manuscript[TITLE],
        AUTHOR: old_manuscript[AUTHOR]
    })
    
    if not old_manu:
        raise ValueError(f"Manuscript not found: {old_manuscript[TITLE]}")

    result = dbc.update(
        collection=MANU_COLLECT,
        filters={
            TITLE: old_manuscript[TITLE],
            AUTHOR: old_manuscript[AUTHOR]
        },
        update_dict={"$set": new_manuscript}
    )
    
    if result.matched_count == 0:
        raise ValueError(f"Manuscript not updated: {old_manuscript[TITLE]}")

    return result


def get_all_manuscripts():
    return dbc.read(MANU_COLLECT)


def get_manuscript_by_title(title):
    result = dbc.fetch_one(MANU_COLLECT, {TITLE: title})
    if not result:
        raise ValueError(f"No matching manuscript for {title}")
    return result


def delete_manuscript(title: str, author: str):
    result = dbc.delete(MANU_COLLECT, {TITLE: title, AUTHOR: author})
    if not result:
        raise ValueError(f"Manuscript not found for Title: {title}, Author: {author}")
    return result

def clear_all_manuscripts():
    deleted_count = dbc.delete(MANU_COLLECT, {})  # Passing an empty filter {} deletes all documents.
    print(f"Deleted {deleted_count} manuscripts.")
    return deleted_count