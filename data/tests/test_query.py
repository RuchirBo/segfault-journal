import random
import pytest
import data.manuscripts.query as mqry
import data.manuscripts.fields as flds


TEST_SAMPLE_MANU = {
    flds.TITLE: 'Testing Title',
    flds.AUTHOR: 'Test Person',
    flds.REFEREES: [],
}

TEST_TITLE = 'First Title'
NOT_TITLE = 'Not Title'

TEST_SAMPLE_INVALID_MANU = {
    flds.TITLE: 'Test Title',
    flds.AUTHOR: 'Test Person',
}

TEST_NEW_VALID_MANU = {
    flds.TITLE: 'New Title',
    flds.AUTHOR: 'New Person',
    flds.REFEREES: [],
}

TEST_OLD_INVALID_MANU = {
    flds.TITLE: 'Non-existent Title',
    flds.AUTHOR: 'Non-existent Author',
    flds.REFEREES: [],
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



def test_create_manuscript_valid():
    result = mqry.create_manuscript(TEST_SAMPLE_MANU)
    assert result == "Manuscript created successfully."
    retrieved_manuscript = mqry.get_manuscript_by_title(TEST_SAMPLE_MANU[flds.TITLE])
    assert retrieved_manuscript[flds.TITLE] == TEST_SAMPLE_MANU[flds.TITLE]
    assert retrieved_manuscript[flds.AUTHOR] == TEST_SAMPLE_MANU[flds.AUTHOR]
    assert retrieved_manuscript[flds.REFEREES] == TEST_SAMPLE_MANU[flds.REFEREES]


def test_create_manuscript_invalid():
    with pytest.raises(ValueError, match="Missing required field for manuscript: referees"):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU)


def test_update_manuscript_valid():
    mqry.update_manuscript(TEST_SAMPLE_MANU, TEST_NEW_VALID_MANU)   
    retrieved_manuscript = mqry.get_manuscript_by_title(TEST_NEW_VALID_MANU[flds.TITLE])
    assert retrieved_manuscript[flds.TITLE] == TEST_NEW_VALID_MANU[flds.TITLE]
    assert retrieved_manuscript[flds.AUTHOR] == TEST_NEW_VALID_MANU[flds.AUTHOR]
    assert retrieved_manuscript[flds.REFEREES] == TEST_NEW_VALID_MANU[flds.REFEREES]


def test_update_manuscript_invalid():
    with pytest.raises(ValueError, match=f"Manuscript not found: {TEST_OLD_INVALID_MANU[flds.TITLE]}"):
        mqry.update_manuscript(TEST_OLD_INVALID_MANU, TEST_NEW_VALID_MANU)


def test_get_all_manuscripts():
    manu = mqry.get_all_manuscripts()
    assert isinstance(manu, list)
    for script in manu:
        assert isinstance(script, dict)


def test_get_manuscript_by_title():
     manuscript = mqry.get_manuscript_by_title("New Title")
     assert manuscript is not None, "Expected manuscript to be returned, but got None"
     assert manuscript[flds.TITLE] == "New Title", f"Expected title 'New Title', but got {manuscript[flds.TITLE]}"
     assert manuscript[flds.AUTHOR] == "New Person", f"Expected author 'New Person', but got {manuscript[flds.AUTHOR]}"


def test_get_manuscript_by_title_invalid():
    with pytest.raises(ValueError, match="No matching manuscript for Not Here"):
        mqry.get_manuscript_by_title("Not Here")


def test_delete_manuscript_valid():
    mqry.delete_manuscript(TEST_SAMPLE_MANU[flds.TITLE], TEST_SAMPLE_MANU[flds.AUTHOR])


def test_delete_manuscript_invalid():
    with pytest.raises(ValueError, match="Manuscript not found for Title: Non-existent Title, Author: Non-existent Author"):
        mqry.delete_manuscript(TEST_OLD_INVALID_MANU[flds.TITLE], TEST_OLD_INVALID_MANU[flds.AUTHOR])
