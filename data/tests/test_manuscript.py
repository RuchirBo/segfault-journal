import random
import pytest
import data.manuscripts.manuscript as mqry
import data.people as ppl


TEST_SAMPLE_MANU = mqry.SAMPLE_MANU

TEST_TITLE = 'First Title'
NOT_TITLE = 'Not Title'

TEST_ED_NAME = "Ted"
TEST_ED_AFF = 'AM'
TEST_ED_ROLES = 'ED'

TEST_SAMPLE_INVALID_MANU_MISSING_FIELDS = {
    mqry.TITLE: 'Test Title',
    mqry.AUTHOR: 'Test Person',
}

TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR_EMAIL = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR_EMAIL[mqry.EDITOR] = 'Ted'

TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR = dict(mqry.SAMPLE_MANU)
TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR[mqry.EDITOR] = 'notgorrister@notrealdomain.net'


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


def test_handle_action_valid_return():
    for state in mqry.get_states():
        for action in mqry.get_valid_actions_by_state(state):
            print(f'{state=}', f'{action=}')
            new_state = mqry.handle_action(state, action,
                                          manu=mqry.SAMPLE_MANU,
                                          ref='Some ref'
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
def test_editor():
    ret = TEST_SAMPLE_MANU[mqry.EDITOR]
    if not ppl.exists(TEST_SAMPLE_MANU[mqry.EDITOR]):
        ppl.create_person(TEST_ED_NAME, TEST_ED_AFF, TEST_SAMPLE_MANU[mqry.EDITOR], TEST_ED_ROLES)
    yield ret
    ppl.delete_person(TEST_SAMPLE_MANU[mqry.EDITOR])

def test_create_manuscript_valid(test_editor):
    result = mqry.create_manuscript(TEST_SAMPLE_MANU)
    assert result == "Manuscript created successfully."
    retrieved_manuscript = mqry.get_manuscript_by_title(TEST_SAMPLE_MANU[mqry.TITLE])
    assert retrieved_manuscript[mqry.TITLE] == TEST_SAMPLE_MANU[mqry.TITLE]
    assert retrieved_manuscript[mqry.AUTHOR] == TEST_SAMPLE_MANU[mqry.AUTHOR]
    assert retrieved_manuscript[mqry.REFEREES] == TEST_SAMPLE_MANU[mqry.REFEREES]

def test_create_manuscript_invalid_missing_fields():
    with pytest.raises(ValueError, match="Missing required field for manuscript: author_email"):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU_MISSING_FIELDS)

def test_create_manuscript_invalid_editor_email():
    with pytest.raises(ValueError, match="Invalid Editor Email: Ted"):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR_EMAIL)

def test_create_manuscript_invalid_editor():
    with pytest.raises(ValueError, match="Editor does not exist with email: notgorrister@notrealdomain.net"):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU_INVALID_EDITOR)

def test_get_manuscript_by_title():
     manuscript = mqry.get_manuscript_by_title(TEST_SAMPLE_MANU[mqry.TITLE])
     assert manuscript is not None, "Expected manuscript to be returned, but got None"
     assert manuscript[mqry.TITLE] == TEST_SAMPLE_MANU[mqry.TITLE], f"Expected title 'Testing Title', but got {manuscript[mqry.TITLE]}"
     assert manuscript[mqry.AUTHOR] == TEST_SAMPLE_MANU[mqry.AUTHOR], f"Expected author 'Test Person', but got {manuscript[mqry.AUTHOR]}"


def test_get_manuscript_by_title_invalid():
    with pytest.raises(ValueError, match="No matching manuscript for Not Here"):
        mqry.get_manuscript_by_title("Not Here")
        

def test_delete_manuscript_valid():
    mqry.delete_manuscript(TEST_SAMPLE_MANU[mqry.TITLE], TEST_SAMPLE_MANU[mqry.AUTHOR])


def test_delete_manuscript_invalid():
    with pytest.raises(ValueError, match="Manuscript not found for Title: Non-existent Title, Author: Non-existent Author"):
        mqry.delete_manuscript(TEST_OLD_INVALID_MANU[mqry.TITLE], TEST_OLD_INVALID_MANU[mqry.AUTHOR])

def test_update_manuscript_valid(test_editor):
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