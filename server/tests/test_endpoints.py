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
        "/people/update/theresa@nyu.edu",
        json={
            "name": "Theresa Updated",
            "email": "theresa@nyu.edu",
            "affiliation": "NYU",
            "roles": "ED",
        }
    )
    assert resp.status_code == 200


@patch('data.manuscripts.query.handle_action', autospec=True,
       return_value='SOME STRING')
def test_handle_action(mock_read):
    resp = TEST_CLIENT.put(f'{ep.MANU_EP}/receive_action',
                           json={
                               flds.TITLE: 'some title',
                               manu.CURR_STATE: 'some state',
                               manu.ACTION: 'some action',
                           })
    assert resp.status_code == OK


@patch("data.text.read_one")
def test_get_text_success(mock_read_one):
    test_key = "some_key"
    mock_text = {"text": "this is some text"}
    mock_read_one.return_value = mock_text

    resp = TEST_CLIENT.get(f"{ep.TEXT_EP}/{test_key}/")
    assert resp.status_code == OK
    assert resp.get_json() == mock_text
    mock_read_one.assert_called_once_with(test_key)


@patch("data.text.create")
def test_create_text_success(mock_create_text):
    payload = {"key": "some_key",
                "title": "some_title",
                "text": "This is some text"}
    resp = TEST_CLIENT.put(f"{ep.TEXT_EP}/create", json=payload)
    assert resp.status_code == OK
    assert resp.get_json() == {"Message":'Text page added!'}


@patch("data.text.read_one", return_value={"key": "some_key", "title": "Old Title", "text": "Old text"})
@patch("data.text.update")
def test_update_text_success(mock_update, mock_read_one):
    payload = {"title": "New Title", "text": "Updated text"}
    resp = TEST_CLIENT.put(f"{ep.TEXT_EP}/some_key/update", json=payload)
    assert resp.status_code == OK
    assert resp.get_json()["Message"] == "Text updated successfully!"
    assert mock_read_one.call_count == 2
    mock_read_one.assert_called_with("some_key")
    mock_update.assert_called_once_with("some_key", "New Title", "Updated text")


@patch("data.text.read_one", return_value=None)
def test_update_text_failure(mock_read_one):
    payload = {"title": "New Title", "text": "Updated text"}
    resp = TEST_CLIENT.put(f"{ep.TEXT_EP}/nonexistent_key/update", json=payload)
    assert resp.status_code == NOT_FOUND
    assert "No text found for key" in resp.get_json()["message"]
    mock_read_one.assert_called_once_with("nonexistent_key")
