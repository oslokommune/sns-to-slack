import re
import json
from slack.cloudwatch_error_to_slack import handler


def test_cloudwatch_error_to_slack(requests_mock):
    message = {
        "AlarmName": "My alarm name",
        "NewStateReason": "My new state reason",
        "StateChangeTime": "2020.01.01",
        "AWSAccountId": "123456",
    }
    event = {"Records": [{"Sns": {"Message": json.dumps(message)}}]}
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False})
    res = handler(event, None)
    assert res is True


def test_cloudwatch_error_to_slack_failing(requests_mock):
    message = {
        "AlarmName": "My alarm name",
        "NewStateReason": "My new state reason",
        "StateChangeTime": "2020.01.01",
        "AWSAccountId": "123456",
    }
    event = {"Records": [{"Sns": {"Message": json.dumps(message)}}]}
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False}, status_code=201)
    try:
        handler(event, None)
    except ValueError:
        assert True
