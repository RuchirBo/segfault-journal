import random
import pytest
import data.manuscripts.query as mqry
import data.manuscripts.fields as flds


TEST_SAMPLE_MANU = {
    flds.TITLE: 'Test Title',
    flds.AUTHOR: 'Test Person',
    flds.REFEREES: [],
}

TEST_TITLE = 'First Title'
NOT_TITLE = 'Not Title'

TEST_SAMPLE_INVALID_MANU = {
    flds.TITLE: 'Test Title',
    flds.AUTHOR: 'Test Person',
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
    mqry.MANUSCRIPTS.clear()
    mqry.create_manuscript(TEST_SAMPLE_MANU)
    assert TEST_SAMPLE_MANU in mqry.MANUSCRIPTS, f"Manuscript was not succesfully added"


def test_create_manuscript_invalid():
    mqry.MANUSCRIPTS.clear()
    with pytest.raises(ValueError, match="Missing required field for manuscript: referees"):
        mqry.create_manuscript(TEST_SAMPLE_INVALID_MANU)


def test_get_all_manuscripts():
    manu = mqry.get_all_manuscripts()
    assert isinstance(manu, list)
    for script in manu:
        assert isinstance(manu, dict)


def test_get_manuscript_by_title():
    mqry.MANUSCRIPTS.clear()
    manuscript = {
        flds.TITLE: 'First Title',
        flds.AUTHOR: 'First Person',
        flds.REFEREES: [],
    }
    mqry.MANUSCRIPTS.append(manuscript)

    manu = mqry.get_manuscript_by_title(TEST_TITLE)
    assert isinstance(manu, dict)
    assert manu[flds.TITLE] == TEST_TITLE

