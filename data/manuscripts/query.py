SUBMITTED = 'SUB'
IN_REF_REV = 'REV'
COPY_EDIT = 'CED'
AUTHOR_REVIEW = 'AUREVIEW'
FORMATTING = 'FORM'
PUBLISHED = 'PUB'
REJECTED = 'REJ'

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
ASSIGN_REF = 'ARF'
DONE = 'DON'
REJECT = 'REJ'
TEST_ACTION = ACCEPT
VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DONE,
    REJECT,
]

FUNC = 'FUNC'

STATE_TABLE = {
    SUBMITTED: {
        ASSIGN_REF: {
            'FUNC': lambda _: IN_REF_REV,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
    },
    IN_REF_REV: {
        ACCEPT: {
            'FUNC': lambda _: COPY_EDIT,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
    },
    COPY_EDIT: {
        DONE: {
            'FUNC': lambda _: AUTHOR_REVIEW,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
    },
    AUTHOR_REVIEW: {
        DONE: {
            'FUNC': lambda _: FORMATTING,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
    },
    FORMATTING: {
        DONE: {
            'FUNC': lambda _: FORMATTING,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
    },
    AUTHOR_REVISIONS: {
        DONE: {
            'FUNC': lambda _: EDITOR_REVIEW,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
    },
    EDITOR_REVIEW: {
        DONE: {
            'FUNC': lambda _: COPY_EDIT,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
    }
}

def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


def handle_action(curr_state, action) -> str:
    if not is_valid_state(curr_state):
        raise ValueError(f'Invalid state: {curr_state}')
    if not is_valid_action(action):
        raise ValueError(f'Invalid action: {action}')
    if curr_state not in STATE_TABLE or action not in STATE_TABLE[curr_state]:
        raise ValueError(f'Invalid action {action} for state {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](None)