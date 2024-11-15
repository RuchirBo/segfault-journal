from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest
from data.people import NAME
import server.endpoints as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


def test_title():
    resp = TEST_CLIENT.get(ep.TITLE_EP)
    resp_json = resp.get_json()
    assert ep.TITLE_RESP in resp_json
    assert isinstance(resp_json[ep.TITLE_RESP], str)
    assert len(resp_json[ep.TITLE_RESP]) > 0


@patch(
    "data.people.read_one",
    return_value={
        "name": "John Doe",
        "roles": [],
        "email": "test@example.com",
    },
)
@patch("data.people.add_role_to_person")
def test_add_role_success(mock_add_role, mock_read_one):
    resp = TEST_CLIENT.post(
        "/people/test@example.com/roles",
        json={"role": "Editor"},
    )
    assert resp.status_code == 200
    assert resp.get_json() == {
        "message": "Role 'Editor' added to test@example.com."
    }
    mock_read_one.assert_called_once_with("test@example.com")
    mock_add_role.assert_called_once_with("test@example.com", "Editor")


@patch(
    "data.people.read_one",
    return_value={
        "name": "John Doe",
        "roles": ["Editor"],
        "email": "test@example.com",
    },
)
@patch("data.people.delete_role_from_person")
def test_remove_role_success(mock_delete_role, mock_read_one):
    resp = TEST_CLIENT.delete(
        "/people/test@example.com/roles",
        json={"role": "Editor"},
    )
    assert resp.status_code == 200
    assert resp.get_json() == {
        "message": "Role 'Editor' removed from test@example.com."
    }
    mock_read_one.assert_called_once_with("test@example.com")
    mock_delete_role.assert_called_once_with("test@example.com", "Editor")
