from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch
from http import HTTPStatus

import pytest
from data.people import NAME
import server.endpoints as ep
# import data.manuscripts.query as manu
# import data.manuscripts.fields as flds
import data.manuscripts.manuscript as manu

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


@patch("data.manuscripts.manuscript.get_manuscript_by_title",
 return_value={"title": "Sample Manuscript"})
def test_get_manuscript_by_title_success(mock_get):
    resp = TEST_CLIENT.get(f"{ep.MANU_EP}/Sample Manuscript")
    assert resp.status_code == OK
    assert resp.get_json() == {"title": "Sample Manuscript"}
    mock_get.assert_called_once_with("Sample Manuscript")


@patch("data.manuscripts.manuscript.get_manuscript_by_title", 
side_effect=ValueError("Manuscript not found"))
def test_get_manuscript_by_title_failure(mock_get):
    resp = TEST_CLIENT.get(f"{ep.MANU_EP}/Nonexistent Manuscript")
    assert resp.status_code == NOT_FOUND
    assert "Manuscript not found" in resp.get_json()["message"]


@patch("data.manuscripts.manuscript.get_manuscript_by_title", return_value={
    manu.TITLE: "Test Manuscript",
    manu.STATE: manu.IN_REF_REV,
    manu.REFEREES: ["ref1@example.com"],
})
@patch("data.manuscripts.manuscript.change_manuscript_state", return_value=manu.COPY_EDIT)
def test_receive_action_success(mock_change_manuscript_state, mock_get_manu):
    """
    Test that the /receive_action endpoint correctly updates a manuscript's state
    when given a valid action.
    """
    payload = {
        manu.TITLE: "Test Manuscript",
        # manu.CURR_STATE: manu.IN_REF_REV,
        manu.ACTION: manu.ACCEPT,
        manu.REFEREES: ["ref1@example.com"]
    }

    resp = TEST_CLIENT.put(f"{ep.MANU_EP}/receive_action", json=payload)
    resp_json = resp.get_json()

    assert resp.status_code == HTTPStatus.OK
    assert resp_json["message"] == "Action received!"
    assert resp_json["title"] == "Test Manuscript"
    assert resp_json["previous_state"] == manu.IN_REF_REV
    assert resp_json["updated_state"] == manu.COPY_EDIT
    assert resp_json["action"] == manu.ACCEPT
    assert resp_json["referees"] == ["ref1@example.com"]
    assert resp_json["forceful_change"] == "N/A"

    mock_get_manu.assert_called_once_with("Test Manuscript")
    mock_change_manuscript_state.assert_called_once_with(
        "Test Manuscript", manu.ACCEPT, manu=mock_get_manu.return_value, ref=["ref1@example.com"], 
    )
