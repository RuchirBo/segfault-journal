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

# TO BE DELETED WHEN UPDATED IN THE STATE TABLE
NOT_TESTED = {REJECTED, WITHDRAWN}

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
    WITHDRAW,
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
        WITHDRAW: {
            'FUNC': lambda _: WITHDRAWN,
        },
    },
    IN_REF_REV: {
        ACCEPT: {
            'FUNC': lambda _: COPY_EDIT,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
        WITHDRAW: {
            'FUNC': lambda _: WITHDRAWN,
        },
    },
    COPY_EDIT: {
        DONE: {
            'FUNC': lambda _: AUTHOR_REVIEW,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
        WITHDRAW: {
            'FUNC': lambda _: WITHDRAWN,
        },
    },
    AUTHOR_REVIEW: {
        DONE: {
            'FUNC': lambda _: FORMATTING,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
        WITHDRAW: {
            'FUNC': lambda _: WITHDRAWN,
        },
    },
    FORMATTING: {
        DONE: {
            'FUNC': lambda _: FORMATTING,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
        WITHDRAW: {
            'FUNC': lambda _: WITHDRAWN,
        },
    },
    AUTHOR_REVISIONS: {
        DONE: {
            'FUNC': lambda _: EDITOR_REVIEW,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
        WITHDRAW: {
            'FUNC': lambda _: WITHDRAWN,
        },
    },
    EDITOR_REVIEW: {
        DONE: {
            'FUNC': lambda _: COPY_EDIT,
        },
        REJECT: {
            'FUNC': lambda _: REJECTED,
        },
        WITHDRAW: {
            'FUNC': lambda _: WITHDRAWN,
        },
    },
    PUBLISHED: {
        DONE: {
            'FUNC': lambda _: PUBLISHED,
        },
        WITHDRAW: {
            'FUNC': lambda _: WITHDRAWN,
        }
    },
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
    if curr_state in NOT_TESTED:
        raise ValueError(f'Cannot perform actions on terminal state: {curr_state}')
    if curr_state not in STATE_TABLE or action not in STATE_TABLE[curr_state]:
        raise ValueError(f'Invalid action {action} for state {curr_state}')
    return STATE_TABLE[curr_state][action][FUNC](manuscript)


def get_valid_actions_by_state(state: str):
    valid_actions = STATE_TABLE[state].keys()
    print(f'{valid_actions=}')
    return valid_actions
