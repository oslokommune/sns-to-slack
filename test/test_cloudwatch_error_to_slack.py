import re
import json
import pytest
from slack.cloudwatch_error_to_slack import (
    handler,
    slackTextFromRecord,
    slackTextFromSnsMessage,
)


message_mock = {
    "AlarmName": "My alarm name",
    "NewStateReason": "My new state reason",
    "StateChangeTime": "2020.01.01",
    "AWSAccountId": "123456",
    "AlarmArn": "arn:aws:cloudwatch:eu-west-1:***REMOVED***:alarm:Dataplatform_LambdaError_s3-writer-is-latest-edition",
    "Trigger": {
        "MetricName": "Errors",
        "Namespace": "AWS/Lambda",
        "StatisticType": "Statistic",
        "Statistic": "SUM",
        "Unit": None,
        "Dimensions": [
            {"value": "s3-writer-dev-is-latest-edition", "name": "FunctionName"},
        ],
        "Period": 60,
        "EvaluationPeriods": 1,
        "ComparisonOperator": "GreaterThanOrEqualToThreshold",
        "Threshold": 1.0,
        "TreatMissingData": "- TreatMissingData: notBreaching",
        "EvaluateLowSampleCountPercentile": "",
    },
}

record_mock = {"EventSource": "aws:sns", "Sns": {"Message": json.dumps(message_mock)}}

event_mock = {"Records": [record_mock]}


def test_cloudwatch_error_to_slack(requests_mock):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False})
    res = handler(event_mock, None)
    assert res is True


def test_cloudwatch_error_to_slack_failing(requests_mock):
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False}, status_code=201)
    with pytest.raises(ValueError):
        handler(event_mock, None)


def test_slack_text_from_record_unsupported_event_source():
    mock = record_mock
    mock["EventSource"] = "aws:asdf"
    with pytest.raises(ValueError):
        slackTextFromRecord(mock)


def test_slack_text_from_sns_nessage():
    text = slackTextFromSnsMessage(message_mock)

    assert "s3-writer-dev-is-latest-edition" in text
    assert "eu-west-1" in text
    assert "Monitoring" in text


def test_slack_text_from_sns_nessage_unsupported_namespace():
    mock = message_mock
    mock["Trigger"]["Namespace"] = "AWS/Kappa"
    with pytest.raises(ValueError):
        slackTextFromSnsMessage(mock)


def test_slack_text_from_sns_nessage_function_name_not_found():
    mock = message_mock
    mock["Trigger"]["Dimensions"] = [{"name": "TheFourth", "value": "lorem-ipsum"}]
    with pytest.raises(ValueError):
        slackTextFromSnsMessage(mock)
