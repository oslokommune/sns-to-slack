import json
import re

import pytest

from slack.cloudwatch_pipeline_state_to_slack import (
    handler,
    get_slack_text,
    check_if_status_is_failed,
)

message_mock = {"detail": {"name": "Failed Event", "status": "FAILED"}}

message_mock_wrong_status = {
    "detail": {"name": "Successful Event", "status": "SUCCESS"}
}

message_mock_no_detail = {}


def make_event(message):
    return {
        "Records": [{"EventSource": "aws:sns", "Sns": {"Message": json.dumps(message)}}]
    }


def test_check_if_status_is_failed():
    assert check_if_status_is_failed(message_mock.get("detail")) is True
    assert check_if_status_is_failed(message_mock_wrong_status.get("detail")) is False


def test_get_slack_text():
    details = message_mock.get("detail")
    assert (
        get_slack_text(message_mock.get("detail"))
        == f"Pipeline with id: {details['name']} failed.\n"
        f"Status is: {details['status']}"
    )


def test_send_event_invalid_source(requests_mock):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False})
    with pytest.raises(ValueError):
        handler({"Records": [{"EventSource": "unknown"}]}, None)


def test_send_empty_event(requests_mock):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False})
    with pytest.raises(ValueError):
        handler({}, None)


def test_send_valid_event(requests_mock):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False})
    res = handler(make_event(message_mock), None)
    assert res is True


def test_send_event_slack_fail(requests_mock):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False}, status_code=201)
    with pytest.raises(ValueError):
        handler(make_event(message_mock), None)


def test_send_event_no_detail(requests_mock):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False})
    res = handler(make_event(message_mock_no_detail), None)
    assert res is False
