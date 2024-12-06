import random
import pytest
import data.manuscripts.query as mqry


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


def test_handle_action_bad_state():
    with pytest.raises(ValueError):
        mqry.handle_action(gen_random_not_valid_str(),
                           mqry.TEST_ACTION,
                           mqry.SAMPLE_MANU)


def test_handle_action_bad_action():
    with pytest.raises(ValueError):
        mqry.handle_action(mqry.TEST_STATE,
                           gen_random_not_valid_str(),
                           mqry.SAMPLE_MANU)


def test_handle_action_valid_return():
    for state in mqry.get_states():
        for action in mqry.get_valid_actions_by_state(state):
            print(f'{action=}')
            new_state = mqry.handle_action(state, action,
                                           mqry.SAMPLE_MANU)
            print(f'{new_state=}')
            assert mqry.is_valid_state(new_state)


def test_withdraw_action():
    for state in mqry.get_states():
        if state not in {mqry.REJECTED, mqry.WITHDRAWN}:
            new_state = mqry.handle_action(state, mqry.WITHDRAW, mqry.SAMPLE_MANU)
            assert new_state == mqry.WITHDRAWN, f"Failed for state {state}"


def test_withdrawn_state_no_actions():
    for action in mqry.get_actions():
        with pytest.raises(ValueError, match="Invalid action"):
            mqry.handle_action(mqry.WITHDRAWN, action, mqry.SAMPLE_MANU)
