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
import data.manuscripts.query as manu
import data.manuscripts.fields as flds

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
        "name": "Yanka Doe",
        "roles": [],
        "email": "testdoe@example.com",
    },
)
@patch("data.people.add_role_to_person")
def test_add_role_success(mock_add_role, mock_read_one):
    resp = TEST_CLIENT.post(
        "/people/testdoe@example.com/roles?role=Editor",  # Use query parameter
    )
    assert resp.status_code == 200
    assert resp.get_json() == {
        "message": "Role 'Editor' added to testdoe@example.com."
    }
    mock_read_one.assert_called_once_with("testdoe@example.com")
    mock_add_role.assert_called_once_with("testdoe@example.com", "Editor")


@patch(
    "data.people.read_one",
    return_value={
        "name": "Yanka Doe",
        "roles": ["Editor"],
        "email": "testdoe@example.com",
    },
)
@patch("data.people.delete_role_from_person")
def test_remove_role_success(mock_delete_role, mock_read_one):
    resp = TEST_CLIENT.delete(
        "/people/testdoe@example.com/roles?role=Editor",  # Use query parameter
    )
    assert resp.status_code == 200
    assert resp.get_json() == {
        "message": "Role 'Editor' removed from testdoe@example.com."
    }
    mock_read_one.assert_called_once_with("testdoe@example.com")
    mock_delete_role.assert_called_once_with("testdoe@example.com", "Editor")

@patch(
    "data.people.read_one",
    return_value={
        "name": "Raiya",
        "roles": ["AU"],
        "email": "rsh9689@nyu.edu",
    },
)
@patch("data.people.delete_person")
def test_delete_person_success(mock_delete_person, mock_read_one):
    resp = TEST_CLIENT.delete(
        "/people/rsh9689@nyu.edu/delete",
    )
    assert resp.status_code == 200
    assert resp.get_json() == {
        "message": 'Person with email rsh9689@nyu.edu was removed.'
    }
    mock_read_one.assert_called_once_with("rsh9689@nyu.edu")
    mock_delete_person.assert_called_once_with("rsh9689@nyu.edu")



@patch("data.people.update_users")
def test_update_person_success(mock_update_users):
    resp = TEST_CLIENT.put(
        "/people/update",
        json={
            "name": "Theresa Updated",
            "email": "theresa@nyu.edu",
            "affiliation": "NYU",
            "roles": "ED",
        }
    )
    assert resp.status_code == 200


@patch('data.query.handle_action', autospec=True,
       return_value='SOME STRING')
def test_handle_action(mock_read):
    resp = TEST_CLIENT.put(f'{ep.MANU_EP}/receive_action',
                           json={
                               flds.TITLE: 'some title',
                               manu.CURR_STATE: 'some state',
                               manu.ACTION: 'some action',
                           })
    assert resp.status_code == OK
