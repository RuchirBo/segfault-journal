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

SAMPLE_MANU = {
    flds.TITLE: 'Test Title',
    flds.AUTHOR: 'Test Person',
    flds.REFEREES: [],
}

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
    manu[flds.REFEREES].append(ref)
    return IN_REF_REV

def delete_ref(manu: dict, ref: str) -> str:
    if len(manu[flds.REFEREES]) > 0:
        manu[flds.REFEREES].remove(ref)
    if len(manu[flds.REFEREES]) > 0:
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


MANUSCRIPTS = [{
    flds.TITLE: 'First Title',
    flds.AUTHOR: 'First Person',
    flds.REFEREES: [],
}]

def create_manuscript(manuscript: dict):
    all_fields = [flds.TITLE, flds.AUTHOR, flds.REFEREES]
    for key in all_fields:
        if key not in manuscript:
            raise ValueError(f"Missing required field for manuscript: {key}")
    MANUSCRIPTS.append(manuscript)


def update_manuscript(old_manuscript: dict, new_manuscript: dict):
    for manu in MANUSCRIPTS:
        if manu[flds.TITLE] == old_manuscript[flds.TITLE] and manu[flds.AUTHOR] == old_manuscript[flds.AUTHOR] and manu[flds.REFEREES] == old_manuscript[flds.REFEREES]:
            manu[flds.TITLE] = new_manuscript[flds.TITLE]
            manu[flds.AUTHOR] = new_manuscript[flds.AUTHOR]
            # manu[flds.REFEREE] = new_manuscript[flds.REFEREE]
        else:
            raise ValueError(f"Manuscript not found: {old_manuscript[flds.TITLE]}")


def get_all_manuscripts():
    return MANUSCRIPTS


def get_manuscript_by_title(title):
    for manuscript in MANUSCRIPTS:
        if manuscript[flds.TITLE].lower() == title.lower():
            return manuscript
    raise ValueError(f"No matching manuscript for {title}")


def delete_manuscript(title: str, author: str):
    for i, manuscript in enumerate(MANUSCRIPTS):
            if (manuscript[flds.TITLE].lower() == title.lower()
                    and manuscript[flds.AUTHOR].lower() == author.lower()):
                del MANUSCRIPTS[i]
                return
    raise ValueError(f"Manuscript not found for Title: {title}, Author: {author}")
