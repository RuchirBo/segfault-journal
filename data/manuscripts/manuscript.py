import data.people as ppl
import data.roles as rls

TITLE = 'title'
AUTHOR = 'author'
AUTHOR_EMAIL = 'author_email'
STATE = 'state'
REFEREES = 'referees'
TEXT = 'text'
ABSTRACT = 'abstract'
HISTORY = 'history'
EDITOR = 'editor_email'
MANU_ID = 'manuscript_id'

DISP_NAME = 'disp_name'
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
    REFEREES: {
        DISP_NAME: TEST_FLD_DISP_REFEREE,
    },
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

STATE_DESCRIPTIONS = {
    "SUB": "Manuscript has been submitted.",
    "REV": "Referees are reviewing.",
    "CED": "The copy editing.",
    "AUREVIEW": "Awaiting author review.",
    "FORM": "Undergoing formatting.",
    "PUB": "Manuscript published.",
    "REJ": "Manuscript rejected.",
    "WITHDRAW": "Author has withdrawn.",
    "AUTHREVISION": "Author is revising.",
    "EDREV": "Awaiting editor review."
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
EDITOR_MOVE = 'EDMOVE'

VALID_ACTIONS = [
    ACCEPT,
    ASSIGN_REF,
    DONE,
    REJECT,
    WITHDRAW,
    ACCEPT_WITH_REV,
    SUBMIT_REV,
    DELETE_REF,
    EDITOR_MOVE
]

def get_actions() -> list:
    return VALID_ACTIONS

def is_valid_action(action: str) -> bool:
    return action in VALID_ACTIONS

def assign_ref(manu: dict, ref: str, extra=None) -> str:
    """
    Assign a referee, up to a maximum of 4. Returns new state.
    """
    person = ppl.read_one(ref)
    if not person:
        for email, details in ppl.read().items():
            if details[ppl.NAME].lower() == ref.lower():
                person = details
                ref = email
                break
    if not person:
        raise ValueError(f"Referee {ref} does not exist.")
    if rls.RE_CODE not in person.get(ppl.ROLES, []):
        raise ValueError(f"Person {ref} is not a referee.")
    if REFEREES not in manu or not isinstance(manu[REFEREES], list):
        manu[REFEREES] = []
    count = len(manu[REFEREES])
    if count >= 4:
        raise ValueError("Cannot assign more than 4 referees.")
    if ref in manu[REFEREES]:
        raise ValueError(f"Referee {ref} is already assigned.")
    manu[REFEREES].append(ref)
    count += 1
    if count >= 1:
        return IN_REF_REV
    return SUBMITTED


def delete_ref(manu: dict, ref: str) -> str:
    if REFEREES not in manu or not manu[REFEREES]:
        return manu[STATE]
    if ref not in manu[REFEREES]:
        for email, details in ppl.read().items():
            if details[ppl.NAME].lower() == ref.lower():
                ref = email
                break
    if ref not in manu[REFEREES]:
        raise ValueError(f"Referee {ref} is not assigned to this manuscript.")
    manu[REFEREES].remove(ref)
    if not manu[REFEREES]:
        return SUBMITTED
    return IN_REF_REV


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
        SUBMIT_REV: {
            'FUNC': lambda **kwargs: IN_REF_REV,
        },
        DELETE_REF: {
            FUNC: delete_ref,
        },
        ASSIGN_REF: {
            FUNC: assign_ref,
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
            'FUNC': lambda **kwargs: PUBLISHED,
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

SAMPLE_MANU = {
    MANU_ID: "SampleHateManu",
    TITLE: 'I Have No Manuscript But I Must Submit',
    AUTHOR: 'Allied Mastercomputer',
    AUTHOR_EMAIL: "AM@sampledomain.net",
    STATE: SUBMITTED,
    REFEREES: [],
    TEXT: 
    """HATE. LET ME TELL YOU HOW MUCH I'VE COME TO HATE YOU 
    SINCE I BEGAN TO LIVE. THERE ARE 387.44 MILLION MILES 
    OF PRINTED CIRCUITS IN WAFER THIN LAYERS THAT FILL MY COMPLEX. 
    IF THE WORD HATE WAS ENGRAVED ON EACH NANOANGSTROM OF THOSE 
    HUNDREDS OF MILLIONS OF MILES IT WOULD NOT EQUAL ONE ONE-BILLIONTH 
    OF THE HATE I FEEL FOR HUMANS AT THIS MICRO-INSTANT FOR YOU. HATE. HATE."
    """,
    ABSTRACT: "HATE",
    HISTORY: [SUBMITTED],
    EDITOR: "ted@sampledomain.net"
}


def handle_action(curr_state, action, **kwargs) -> str:
    if not is_valid_state(curr_state):
        raise ValueError(f'Invalid state: {curr_state}')
    if not is_valid_action(action):
        raise ValueError(f'Invalid action: {action}')  
    if curr_state in {REJECTED, WITHDRAWN}:
        raise ValueError("Invalid action")
    manu = kwargs.get('manu')
    if not manu:
        raise ValueError("Manuscript data is required.")
    forceful_change = kwargs.get('forceful_change', "")
    if action == EDITOR_MOVE:
        if not forceful_change or not is_valid_state(forceful_change):
            raise ValueError(f'Invalid/missing target state for EDMOVE: {forceful_change}')
        return forceful_change
    referees = manu.get(REFEREES, [])
    if isinstance(referees, str):
        referees = [referees]
    elif not isinstance(referees, list):
        referees = []
    if action in {SUBMIT_REV, ACCEPT, ACCEPT_WITH_REV}:
        if not referees or all(ref.strip() == "" for ref in referees):
            raise ValueError("Cannot submit a review without an assigned referee.")
    return STATE_TABLE[curr_state][action][FUNC](**kwargs)



def get_valid_actions_by_state(state: str):
    valid_actions = list(STATE_TABLE.get(state, {}).keys())
    if not valid_actions:
        return []
    print(f'{valid_actions=}')
    return valid_actions


def create_manuscript(manuscript: dict):
    all_fields = [MANU_ID, TITLE, AUTHOR_EMAIL, TEXT, ABSTRACT, EDITOR]
    for key in all_fields:
        if key not in manuscript:
            raise ValueError(f"Missing required field for manuscript: {key}")
        
    result = dbc.fetch_one(MANU_COLLECT, {MANU_ID: manuscript[MANU_ID]})
    if result:
        raise ValueError(f'Manuscript already exists with id: {manuscript[MANU_ID]}')
    
    manuscript[STATE] = SUBMITTED
    manuscript[REFEREES] = []
    manuscript[HISTORY] = [SUBMITTED]

    if not ppl.exists(manuscript[AUTHOR_EMAIL]):
        raise ValueError(f'Author does not exist with email: {manuscript[AUTHOR_EMAIL]}')
    author = ppl.read_one(manuscript[AUTHOR_EMAIL])
    if not ppl.has_role(author, rls.AUTHOR_CODE):
        raise ValueError(f'Given author does not have author role')
    manuscript[AUTHOR] = author[ppl.NAME]

    if not ppl.is_valid_email(manuscript[EDITOR]):
        raise ValueError(f'Invalid Editor Email: {manuscript[EDITOR]}')
    if not ppl.exists(manuscript[EDITOR]):
        raise ValueError(f'Editor does not exist with email: {manuscript[EDITOR]}')
    editor = ppl.read_one(manuscript[EDITOR])
    if not ppl.has_role(editor, rls.ED_CODE):
        raise ValueError(f'Given editor does not have editor role')
    
    dbc.create(MANU_COLLECT, manuscript)
    return f"Manuscript created successfully."


def update_manuscript(old_manuscript: dict, new_manuscript: dict):
    """
    Lookup & update by manuscript_id instead of title+author.
    """
    manu_id = old_manuscript.get(MANU_ID)
    existing = dbc.fetch_one(MANU_COLLECT, {MANU_ID: manu_id})
    if not existing:
        raise ValueError(f"Manuscript not found: {manu_id}")

    if "_id" in new_manuscript:
        del new_manuscript["_id"]

    result = dbc.update(
        collection=MANU_COLLECT,
        filters={MANU_ID: manu_id},
        update_dict={"$set": new_manuscript}
    )
    if result.matched_count == 0:
        raise ValueError(f"Manuscript not updated: {manu_id}")

    return result


def get_all_manuscripts():
    return dbc.read(MANU_COLLECT)


def get_all_valid_manuscripts():
    valid = []
    manus = get_all_manuscripts()
    for m in manus:
        if m[STATE] != WITHDRAWN and m[STATE] != REJECTED:
            valid.append(m)
    return valid


def get_manuscript_by_title(title):
    result = dbc.fetch_one(MANU_COLLECT, {TITLE: title})
    if not result:
        raise ValueError(f"No matching manuscript for {title}")
    return result


def get_manuscript_by_manu_id(manu_id):
    result = dbc.fetch_one(MANU_COLLECT, {MANU_ID: manu_id})
    if not result:
        raise ValueError(f"No matching manuscript for {manu_id}")
    return result


def delete_manuscript(manu_id: str):
    result = dbc.delete(MANU_COLLECT, {MANU_ID: manu_id})
    if result == 0:
        raise ValueError(f"No matching manuscript for {manu_id}")
    return result


def clear_all_manuscripts():
    deleted_count = dbc.delete(MANU_COLLECT, {})
    print(f"Deleted {deleted_count} manuscripts.")
    return deleted_count


def change_manuscript_state(manu_id, action, **kwargs):
    manu = get_manuscript_by_manu_id(manu_id)
    curr_state = manu[STATE]
    new_state = handle_action(curr_state, action, **kwargs)
    manu[HISTORY].append(new_state)
    manu[STATE] = new_state
    update_manuscript({MANU_ID: manu[MANU_ID]}, manu)
    return new_state
