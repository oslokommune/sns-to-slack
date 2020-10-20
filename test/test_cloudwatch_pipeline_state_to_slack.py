import re
import pytest
from slack.cloudwatch_pipeline_state_to_slack import (
    handler,
    get_slack_text,
    check_if_status_is_failed,
)

event_mock = {"detail": {"name": "Failed Event", "status": "FAILED"}}

event_mock_wrong_status = {"detail": {"name": "Successful Event", "status": "SUCCESS"}}

event_mock_no_detail = {}


def test_check_if_status_is_failed():
    assert check_if_status_is_failed(event_mock.get("detail")) is True
    assert check_if_status_is_failed(event_mock_wrong_status.get("detail")) is False


def test_get_slack_text():
    details = event_mock.get("detail")
    assert (
        get_slack_text(event_mock.get("detail"))
        == f"Pipeline with id: {details['name']} failed.\n"
        f"Status is: {details['status']}"
    )


def test_handler(requests_mock):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False})
    res = handler(event_mock, None)
    assert res is True


def test_handler_slack_fail(requests_mock):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False}, status_code=201)
    with pytest.raises(ValueError):
        handler(event_mock, None)


def test_handler_no_detail(requests_mock):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False})
    res = handler(event_mock_no_detail, None)
    assert res is False
