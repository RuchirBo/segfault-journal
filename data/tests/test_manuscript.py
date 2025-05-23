import random
import pytest
import data.manuscripts.manuscript as mqry
import data.people as ppl
from unittest.mock import patch
import data.roles as rls


# Constants
TEST_SAMPLE_MANU = mqry.SAMPLE_MANU

TEST_TITLE = 'First Title'
NOT_TITLE = 'Not Title'

TEST_AU_ROLES = [rls.AUTHOR_CODE]

TEST_ED_NAME = "Ted"
TEST_ED_AFF = 'AM'
TEST_ED_ROLES = [rls.ED_CODE]
TEST_PASSWORD = 'pass'

TEST_SAMPLE_INVALID_MANU_MISSING_FIELDS = {
    mqry.TITLE: 'Test Title',
    mqry.AUTHOR: 'Test Person',
}

TEST_SAMPLE_INVALID_MANU_INVALID_AUTHOR = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_INVALID_AUTHOR[mqry.AUTHOR_EMAIL] = 'notrightperson@nuhuh.net'
TEST_SAMPLE_INVALID_MANU_INVALID_AUTHOR[mqry.MANU_ID] = 'InvalidManu'

TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR_EMAIL = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR_EMAIL[mqry.EDITOR] = 'Ted'
TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR_EMAIL[mqry.MANU_ID] = 'InvalidManu'

TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR[mqry.EDITOR] = 'notgorrister@notrealdomain.net'
TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR[mqry.MANU_ID] = 'InvalidManu'

TEST_SAMPLE_INVALID_MANU_AUTHOR_ROLE = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_AUTHOR_ROLE[mqry.AUTHOR_EMAIL] = mqry.SAMPLE_MANU[mqry.EDITOR]
TEST_SAMPLE_INVALID_MANU_AUTHOR_ROLE[mqry.MANU_ID] = 'InvalidManu'

TEST_SAMPLE_INVALID_MANU_EDITOR_ROLE = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_EDITOR_ROLE[mqry.EDITOR] = mqry.SAMPLE_MANU[mqry.AUTHOR_EMAIL]
TEST_SAMPLE_INVALID_MANU_EDITOR_ROLE[mqry.MANU_ID] = 'InvalidManu'


TEST_NEW_VALID_MANU = dict(mqry.SAMPLE_MANU)
TEST_NEW_VALID_MANU[mqry.TITLE] = "I Have No Manuscript But I Must Update"

TEST_OLD_INVALID_MANU = {
    mqry.MANU_ID: 'Non-existent ManuID',
    mqry.TITLE: 'Non-existent Title',
    mqry.AUTHOR: 'Non-existent Author',
    mqry.REFEREES: [],
}


def gen_random_not_valid_str() -> str:
    BIG_NUM = 50_000_000_000
    big_int = random.randint(0, BIG_NUM)
    big_int += BIG_NUM
    bad_str = str(big_int)
    return bad_str


def test_is_valid_state():
    for state in mqry.get_states():
        assert mqry.is_valid_state(state)


def test_is_valid_action():
    for action in mqry.get_actions():
        assert mqry.is_valid_action(action)


def test_is_invalid_action():
    for i in range(10):
        assert not mqry.is_valid_action(gen_random_not_valid_str())


def test_is_invalid_action_for_state():
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.REJECTED,
                           mqry.REJECT,
                           manu=mqry.SAMPLE_MANU)


def test_handle_action_bad_state():
    with pytest.raises(ValueError):
        mqry.handle_action(gen_random_not_valid_str(),
                           mqry.TEST_ACTION,
                           manu=mqry.SAMPLE_MANU)


def test_reject_action():
    for state in mqry.get_states():
        if state in {mqry.SUBMITTED, mqry.IN_REF_REV}:
            new_state = mqry.handle_action(state, mqry.REJECT, manu=mqry.SAMPLE_MANU)
            assert new_state == mqry.REJECTED, f"Failed for state {state}"


def test_rejected_state_no_actions():
    for action in mqry.get_actions():
        with pytest.raises(ValueError, match="Invalid action"):
            mqry.handle_action(mqry.REJECTED, action,manu=mqry.SAMPLE_MANU)


def test_handle_action_bad_action():
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.TEST_STATE,
                           gen_random_not_valid_str(),
                           manu=mqry.SAMPLE_MANU)


@patch("data.people.read_one", return_value={"email": "tom@gmail.com", "roles": [rls.RE_CODE]})
@patch("data.people.read", return_value={"tom@gmail.com": {"email": "tom@gmail.com", "roles": [rls.RE_CODE]}})
def test_handle_action_valid_return(mock_read_one, mock_read):
    for state in mqry.get_states():
        for action in mqry.get_valid_actions_by_state(state):
            print(f'{state=}', f'{action=}')
            new_state = mqry.handle_action(state, action,
                                           manu=mqry.SAMPLE_MANU,
                                           ref='tom'
                                           )
            print(f'{new_state=}')
            assert mqry.is_valid_state(new_state)


def test_withdraw_action():
    for state in mqry.get_states():
        if state not in {mqry.REJECTED, mqry.WITHDRAWN, mqry.PUBLISHED}:
            new_state = mqry.handle_action(state, mqry.WITHDRAW,manu=mqry.SAMPLE_MANU)
            assert new_state == mqry.WITHDRAWN, f"Failed for state {state}"


def test_withdrawn_state_no_actions():
    for action in mqry.get_actions():
        with pytest.raises(ValueError, match="Invalid action"):
            mqry.handle_action(mqry.WITHDRAWN, action,manu=mqry.SAMPLE_MANU)


@pytest.fixture(scope='function')
def test_people():
    author_email = TEST_SAMPLE_MANU[mqry.AUTHOR_EMAIL]
    editor_email = TEST_SAMPLE_MANU[mqry.EDITOR]
    
    author_existed = ppl.exists(author_email)
    editor_existed = ppl.exists(editor_email)
    
    if author_existed:
        original_author = ppl.read_one(author_email)
        ppl.delete_person(author_email)
    
    if editor_existed:
        original_editor = ppl.read_one(editor_email)
        ppl.delete_person(editor_email)
    
    ppl.create_person(
        TEST_SAMPLE_MANU[mqry.AUTHOR],
        TEST_ED_AFF,
        author_email,
        TEST_PASSWORD,       
        TEST_AU_ROLES          
    )
    
    author_person = ppl.read_one(author_email)
    assert rls.AUTHOR_CODE in author_person.get('roles', []), "Author role wasn't properly assigned"
    
    ppl.create_person(
        TEST_ED_NAME,                 
        TEST_ED_AFF,                   
        editor_email,                  
        TEST_PASSWORD,               
        TEST_ED_ROLES                   
    )
    
    editor_person = ppl.read_one(editor_email)
    assert rls.ED_CODE in editor_person.get('roles', []), "Editor role wasn't properly assigned"

    if not mqry.exists(TEST_SAMPLE_MANU[mqry.MANU_ID]):
        mqry.create_manuscript(TEST_SAMPLE_MANU)
    
    yield author_email, editor_email
    
    if mqry.exists(TEST_SAMPLE_MANU[mqry.MANU_ID]):
        mqry.delete_manuscript(TEST_SAMPLE_MANU[mqry.MANU_ID])
    
    ppl.delete_person(author_email)
    ppl.delete_person(editor_email)
    
    if author_existed:
        ppl.create_person(
            original_author.get('name', ''),
            original_author.get('affiliation', ''),
            original_author.get('email', ''),
            original_author.get('password', ''),
            original_author.get('roles', [])
        )
    
    if editor_existed:
        ppl.create_person(
            original_editor.get('name', ''),
            original_editor.get('affiliation', ''),
            original_editor.get('email', ''),
            original_editor.get('password', ''),
            original_editor.get('roles', [])
        )


def test_create_manuscript_valid(test_people):
    retrieved_manuscript = mqry.get_manuscript_by_manu_id(TEST_SAMPLE_MANU[mqry.MANU_ID])
    assert retrieved_manuscript[mqry.TITLE] == TEST_SAMPLE_MANU[mqry.TITLE]
    assert retrieved_manuscript[mqry.AUTHOR] == TEST_SAMPLE_MANU[mqry.AUTHOR]
    assert retrieved_manuscript[mqry.REFEREES] == TEST_SAMPLE_MANU[mqry.REFEREES]


def test_create_manuscript_invalid_manu_id(test_people):
    with pytest.raises(ValueError, match="Manuscript already exists with id: SampleHateManu"):
        mqry.create_manuscript(TEST_SAMPLE_MANU)


def test_create_manuscript_invalid_missing_fields(test_people):
    with pytest.raises(ValueError, match="Missing required field for manuscript: manuscript_id"):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU_MISSING_FIELDS)


def test_create_manuscript_invalid_author(test_people):
    with pytest.raises(ValueError, match="Author does not exist with email: notrightperson@nuhuh.net"):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU_INVALID_AUTHOR)


def test_create_manuscript_invalid_editor_email(test_people):
    with pytest.raises(ValueError, match="Invalid Editor Email: Ted"):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR_EMAIL)


def test_create_manuscript_invalid_editor(test_people):
    with pytest.raises(ValueError, match="Editor does not exist with email: notgorrister@notrealdomain.net"):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR)


def test_create_manuscript_invalid_author_role(test_people):
    with pytest.raises(ValueError, match='Given author does not have author role'):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU_AUTHOR_ROLE)


def test_create_manuscript_invalid_editor_role(test_people):
    with pytest.raises(ValueError, match='Given editor does not have editor role'):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU_EDITOR_ROLE)


def test_get_manuscript_by_title(test_people):
    manuscript = mqry.get_manuscript_by_title(TEST_SAMPLE_MANU[mqry.TITLE])
    assert manuscript is not None, "Expected manuscript to be returned, but got None"
    assert manuscript[mqry.TITLE] == TEST_SAMPLE_MANU[mqry.TITLE], f"Expected title {TEST_SAMPLE_MANU[mqry.TITLE]}, but got {manuscript[mqry.TITLE]}"
    assert manuscript[mqry.AUTHOR] == TEST_SAMPLE_MANU[mqry.AUTHOR], f"Expected author {TEST_SAMPLE_MANU[mqry.AUTHOR]}, but got {manuscript[mqry.AUTHOR]}"


def test_get_manuscript_by_title_invalid():
    with pytest.raises(ValueError, match="No matching manuscript for Not Here"):
        mqry.get_manuscript_by_title("Not Here")


def test_get_manuscript_by_manu_id_valid(test_people):
    manuscript = mqry.get_manuscript_by_manu_id(TEST_SAMPLE_MANU[mqry.MANU_ID])
    assert manuscript is not None, "Expected manuscript to be returned, but got None"
    assert manuscript[mqry.TITLE] == TEST_SAMPLE_MANU[mqry.TITLE], f"Expected title {TEST_SAMPLE_MANU[mqry.TITLE]}, but got {manuscript[mqry.TITLE]}"
    assert manuscript[mqry.MANU_ID] == TEST_SAMPLE_MANU[mqry.MANU_ID], f"Expected manuscript_id {TEST_SAMPLE_MANU[mqry.MANU_ID]}, but got {manuscript[mqry.MANU_ID]}"


def test_change_manuscript_state_rej(test_people):
    old_manu = mqry.get_manuscript_by_manu_id(TEST_SAMPLE_MANU[mqry.MANU_ID])
    print(f"Old Manuscript: {old_manu}")
    mqry.change_manuscript_state(TEST_SAMPLE_MANU[mqry.MANU_ID], mqry.REJECT, manu=old_manu)
    new_manu = mqry.get_manuscript_by_manu_id(TEST_SAMPLE_MANU[mqry.MANU_ID])
    assert new_manu[mqry.STATE] == mqry.REJECTED, f"Expected state 'REJ', but got {new_manu[mqry.STATE]}"
    expected_history = old_manu[mqry.HISTORY] + [mqry.REJECT]
    assert new_manu[mqry.HISTORY] == expected_history, f"History mismatch: {new_manu[mqry.HISTORY]}"
