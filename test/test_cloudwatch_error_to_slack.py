import re
import json
from slack.cloudwatch_error_to_slack import handler


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


def test_cloudwatch_error_to_slack(requests_mock):
    event = {"Records": [{"Sns": {"Message": json.dumps(message_mock)}}]}
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False})
    res = handler(event, None)
    assert res is True


def test_cloudwatch_error_to_slack_failing(requests_mock):
    event = {"Records": [{"Sns": {"Message": json.dumps(message_mock)}}]}
    matcher = re.compile("slack")
    requests_mock.register_uri("POST", matcher, json={"access": False}, status_code=201)
    try:
        handler(event, None)
    except ValueError:
        assert True
