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


def get_actions() -> list:
    return VALID_ACTIONS


def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS


def handle_action(curr_state, action) -> str:
    if not is_valid_state(curr_state):
        raise ValueError(f'Invalid state: {curr_state}')
    if not is_valid_action(action):
        raise ValueError(f'Invalid action: {action}')
    new_state = curr_state
    if curr_state == SUBMITTED:
        if action == ASSIGN_REF:
            new_state = IN_REF_REV
        elif action == REJECT:
            new_state = REJECTED
    elif curr_state == IN_REF_REV:
        if action == ACCEPT:
            new_state = COPY_EDIT
        elif action == REJECT:
            new_state = REJECTED
    elif curr_state == COPY_EDIT:
        if action == DONE:
            new_state = AUTHOR_REVIEW
        elif action == REJECT:
            new_state = REJECTED
    elif curr_state == AUTHOR_REVIEW:
        if action == DONE:
            new_state = FORMATTING
        elif action == REJECT:
            new_state = REJECTED
    elif curr_state == FORMATTING:
        if action == DONE:
            new_state = PUBLISHED
        elif action == REJECT:
            new_state = REJECTED
    elif curr_state == AUTHOR_REVISIONS:
        if action == DONE:
            new_state = EDITOR_REVIEW
        elif action == REJECT:
            new_state = REJECTED
    elif curr_state == EDITOR_REVIEW:
        if action == ACCEPT:
            new_state = COPY_EDIT
        elif action == REJECT:
            new_state = REJECTED
    return new_state