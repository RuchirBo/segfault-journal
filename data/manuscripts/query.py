import data.manuscripts.fields as flds
SUBMITTED = 'SUB'
IN_REF_REV = 'REV'
COPY_EDIT = 'CED'
AUTHOR_REVIEW = 'AUREVIEW'
FORMATTING = 'FORM'
PUBLISHED = 'PUB'
REJECTED = 'REJ'
WITHDRAW = 'WITHDRAW'

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
REMOVE_REF = 'REMREF'
TEST_ACTION = ACCEPT
VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DONE,
    REJECT,
    WITHDRAW,
    ACCEPT_WITH_REV,
    SUBMIT_REV,
    REMOVE_REF
]

FUNC = 'FUNC'

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            'FUNC': lambda m: IN_REF_REV,
        },
        REJECT: {
            'FUNC': lambda m: REJECTED,
        },
        WITHDRAW: {
            'FUNC': lambda m: WITHDRAWN,
        },
    },
    IN_REF_REV: {
        ACCEPT: {
            'FUNC': lambda m: COPY_EDIT,
        },
        ACCEPT_WITH_REV: {
            'FUNC': lambda m: AUTHOR_REVISIONS,
        },
        ASSIGN_REF: {
            'FUNC': lambda m: IN_REF_REV,
        },
        SUBMIT_REV: {
            'FUNC': lambda m: IN_REF_REV,
        },
        REMOVE_REF: {
            'FUNC': lambda m: IN_REF_REV,
        },
        REJECT: {
            'FUNC': lambda m: REJECTED,
        },
        WITHDRAW: {
            'FUNC': lambda m: WITHDRAWN,
        },
    },
    COPY_EDIT: {
        DONE: {
            'FUNC': lambda m: AUTHOR_REVIEW,
        },
        WITHDRAW: {
            'FUNC': lambda m: WITHDRAWN,
        },
    },
    AUTHOR_REVIEW: {
        DONE: {
            'FUNC': lambda m: FORMATTING,
        },
        WITHDRAW: {
            'FUNC': lambda m: WITHDRAWN,
        },
    },
    FORMATTING: {
        DONE: {
            'FUNC': lambda m: FORMATTING,
        },
        WITHDRAW: {
            'FUNC': lambda m: WITHDRAWN,
        },
    },
    AUTHOR_REVISIONS: {
        DONE: {
            'FUNC': lambda m: EDITOR_REVIEW,
        },
        WITHDRAW: {
            'FUNC': lambda m: WITHDRAWN,
        },
    },
    EDITOR_REVIEW: {
        ACCEPT: {
            'FUNC': lambda m: COPY_EDIT,
        },
        WITHDRAW: {
            'FUNC': lambda m: WITHDRAWN,
        },
    },
    PUBLISHED: {},
    REJECTED:{},
    WITHDRAWN:{}
}

def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


SAMPLE_MANU = {
    flds.TITLE: 'Test Title',
    flds.AUTHOR: 'Test Person',
    flds.REFEREES: [],
}


def handle_action(curr_state, action, manuscript) -> str:
    if not is_valid_state(curr_state):
        raise ValueError(f'Invalid state: {curr_state}')
    if not is_valid_action(action):
        raise ValueError(f'Invalid action: {action}')
    if curr_state not in STATE_TABLE or action not in STATE_TABLE[curr_state]:
        raise ValueError(f'Invalid action {action} for state {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](manuscript)


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions
