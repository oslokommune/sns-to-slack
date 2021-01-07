import re

import pytest

from slack.handler import cloudwatch_error_to_slack


def test_cloudwatch_error_to_slack(requests_mock, lambda_event):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"anccess": False})
    assert cloudwatch_error_to_slack(lambda_event, None)


def test_cloudwatch_error_to_slack_failing(requests_mock, lambda_event):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False}, status_code=201)
    with pytest.raises(ValueError):
        cloudwatch_error_to_slack(lambda_event, None)


def test_slack_text_from_record_unsupported_event_source(lambda_event):
    lambda_event["Records"][0]["EventSource"] = "aws:asdf"
    with pytest.raises(ValueError):
        cloudwatch_error_to_slack(lambda_event, None)


def test_slack_text_from_sns_nessage_unsupported_namespace(unknown_namespace_event):
    with pytest.raises(ValueError):
        cloudwatch_error_to_slack(unknown_namespace_event, None)
