import random
import pytest
import data.manuscripts.manuscript as mqry
import data.people as ppl
from unittest.mock import patch
import data.roles as rls


TEST_SAMPLE_MANU = mqry.SAMPLE_MANU

TEST_TITLE = 'First Title'
NOT_TITLE = 'Not Title'

TEST_AU_ROLES = [rls.AUTHOR_CODE]

TEST_ED_NAME = "Ted"
TEST_ED_AFF = 'AM'
TEST_ED_ROLES = [rls.ED_CODE]

TEST_SAMPLE_INVALID_MANU_MISSING_FIELDS = {
    mqry.TITLE: 'Test Title',
    mqry.AUTHOR: 'Test Person',
}

TEST_SAMPLE_INVALID_MANU_INVALID_AUTHOR = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_INVALID_AUTHOR[mqry.AUTHOR_EMAIL] = 'notrightperson@nuhuh.net'

TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR_EMAIL = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR_EMAIL[mqry.EDITOR] = 'Ted'

TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR[mqry.EDITOR] = 'notgorrister@notrealdomain.net'

TEST_SAMPLE_INVALID_MANU_AUTHOR_ROLE = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_AUTHOR_ROLE[mqry.AUTHOR_EMAIL] = mqry.SAMPLE_MANU[mqry.EDITOR]

TEST_SAMPLE_INVALID_MANU_EDITOR_ROLE = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_EDITOR_ROLE[mqry.EDITOR] = mqry.SAMPLE_MANU[mqry.AUTHOR_EMAIL]


TEST_NEW_VALID_MANU = {
    mqry.TITLE: 'New Title',
    mqry.AUTHOR: 'New Person',
    mqry.REFEREES: [],
}

TEST_OLD_INVALID_MANU = {
    mqry.TITLE: 'Non-existent Title',
    mqry.AUTHOR: 'Non-existent Author',
    mqry.REFEREES: [],
}


def gen_random_not_valid_str() -> str:
    BIG_NUM = 50_000_000_000
    big_int = random.randint(0, BIG_NUM)
    big_int += BIG_NUM
    bad_str = str(big_int)


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
    ret_author = TEST_SAMPLE_MANU[mqry.AUTHOR_EMAIL]
    if not ppl.exists(TEST_SAMPLE_MANU[mqry.AUTHOR_EMAIL]):
        ppl.create_person(TEST_SAMPLE_MANU[mqry.AUTHOR], TEST_ED_AFF, TEST_SAMPLE_MANU[mqry.AUTHOR_EMAIL], TEST_AU_ROLES)
    ret_editor = TEST_SAMPLE_MANU[mqry.EDITOR]
    if not ppl.exists(TEST_SAMPLE_MANU[mqry.EDITOR]):
        ppl.create_person(TEST_ED_NAME, TEST_ED_AFF, TEST_SAMPLE_MANU[mqry.EDITOR], TEST_ED_ROLES)
    yield ret_author, ret_editor
    ppl.delete_person(TEST_SAMPLE_MANU[mqry.AUTHOR_EMAIL])
    ppl.delete_person(TEST_SAMPLE_MANU[mqry.EDITOR])

def test_create_manuscript_valid(test_people):
    result = mqry.create_manuscript(TEST_SAMPLE_MANU)
    assert result == "Manuscript created successfully."
    retrieved_manuscript = mqry.get_manuscript_by_title(TEST_SAMPLE_MANU[mqry.TITLE])
    assert retrieved_manuscript[mqry.TITLE] == TEST_SAMPLE_MANU[mqry.TITLE]
    assert retrieved_manuscript[mqry.AUTHOR] == TEST_SAMPLE_MANU[mqry.AUTHOR]
    assert retrieved_manuscript[mqry.REFEREES] == TEST_SAMPLE_MANU[mqry.REFEREES]

def test_create_manuscript_invalid_missing_fields(test_people):
    with pytest.raises(ValueError, match="Missing required field for manuscript: author_email"):
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

def test_get_manuscript_by_title():
     manuscript = mqry.get_manuscript_by_title(TEST_SAMPLE_MANU[mqry.TITLE])
     assert manuscript is not None, "Expected manuscript to be returned, but got None"
     assert manuscript[mqry.TITLE] == TEST_SAMPLE_MANU[mqry.TITLE], f"Expected title 'Testing Title', but got {manuscript[mqry.TITLE]}"
     assert manuscript[mqry.AUTHOR] == TEST_SAMPLE_MANU[mqry.AUTHOR], f"Expected author 'Test Person', but got {manuscript[mqry.AUTHOR]}"


def test_get_manuscript_by_title_invalid():
    with pytest.raises(ValueError, match="No matching manuscript for Not Here"):
        mqry.get_manuscript_by_title("Not Here")


def test_change_manuscript_state_rej():
    old_manu = mqry.get_manuscript_by_title(TEST_SAMPLE_MANU[mqry.TITLE])
    print(old_manu)
    mqry.change_manuscript_state(TEST_SAMPLE_MANU[mqry.TITLE], mqry.REJECT, manu = old_manu)
    new_manu = mqry.get_manuscript_by_title(TEST_SAMPLE_MANU[mqry.TITLE])
    assert new_manu[mqry.STATE] == mqry.REJECTED, f"Expected state 'REJ', but got {manu[mqry.STATE]}"
    assert new_manu[mqry.HISTORY] == [mqry.SUBMITTED, mqry.REJECTED], f"Expected history ['SUB', 'REJ'], but got {manu[mqry.HISTORY]}"
        

def test_delete_manuscript_valid():
    mqry.delete_manuscript(TEST_SAMPLE_MANU[mqry.TITLE], TEST_SAMPLE_MANU[mqry.AUTHOR])


def test_delete_manuscript_invalid():
    with pytest.raises(ValueError, match="Manuscript not found for Title: Non-existent Title, Author: Non-existent Author"):
        mqry.delete_manuscript(TEST_OLD_INVALID_MANU[mqry.TITLE], TEST_OLD_INVALID_MANU[mqry.AUTHOR])

def test_update_manuscript_valid(test_people):
    mqry.create_manuscript(TEST_SAMPLE_MANU)
    mqry.update_manuscript(TEST_SAMPLE_MANU, TEST_NEW_VALID_MANU)   
    print(mqry.get_all_manuscripts())
    retrieved_manuscript = mqry.get_manuscript_by_title(TEST_NEW_VALID_MANU[mqry.TITLE])
    assert retrieved_manuscript[mqry.TITLE] == TEST_NEW_VALID_MANU[mqry.TITLE]
    assert retrieved_manuscript[mqry.AUTHOR] == TEST_NEW_VALID_MANU[mqry.AUTHOR]
    assert retrieved_manuscript[mqry.REFEREES] == TEST_NEW_VALID_MANU[mqry.REFEREES]


def test_update_manuscript_invalid():
    with pytest.raises(ValueError, match=f"Manuscript not found: {TEST_OLD_INVALID_MANU[mqry.TITLE]}"):
        mqry.update_manuscript(TEST_OLD_INVALID_MANU, TEST_NEW_VALID_MANU)


def test_get_all_manuscripts():
    manu = mqry.get_all_manuscripts()
    assert isinstance(manu, list)
    for script in manu:
        assert isinstance(script, dict)

def test_clear_all_manuscripts():
    mqry.clear_all_manuscripts()
    print(mqry.get_all_manuscripts())