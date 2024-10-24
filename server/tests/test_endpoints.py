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

# def test_update():
#     people = TEST_CLIENT.read()
#     assert ADD_EMAIL not in people
#     TEST_CLIENT.create('Joe Smith', 'NYU', ADD_EMAIL)
#     people = TEST_CLIENT.read()
#     assert ADD_EMAIL in people


# def test_get_people():
#     resp = TEST_CLIENT.get(ep.PEOPLE_EP)
#     print(f'{id(resp)=}')
#     print(f'{ep.PEOPLE_EP=}')
#     resp_json = resp.get_json()
#     for _id in resp_json:
#         pass
#     assert False