import json

import pytest


@pytest.fixture
def lambda_message():
    return {
        "AlarmName": "My alarm name",
        "NewStateReason": "My new state reason",
        "StateChangeTime": "2020.01.01",
        "AWSAccountId": "123456",
        "AlarmArn": "arn:aws:cloudwatch:eu-west-1:123456789000:alarm:Dataplatform_LambdaError_s3-writer-is-latest-edition",
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


@pytest.fixture
def sqs_message():
    return {
        "AlarmName": "Dataplatform_DeadLetterQueue",
        "AlarmDescription": None,
        "AWSAccountId": "123456",
        "AlarmConfigurationUpdatedTimestamp": "2025-08-12T11:42:35.135+0000",
        "NewStateValue": "ALARM",
        "NewStateReason": "Threshold Crossed: 1 datapoint [1.0 (13/08/25 08:07:00)] was greater than or equal to the threshold (1.0).",
        "StateChangeTime": "2025-08-13T08:08:23.374+0000",
        "Region": "EU (Ireland)",
        "AlarmArn": "arn:aws:cloudwatch:eu-west-1:123456789000:alarm:Dataplatform_DeadLetterQueue",
        "OldStateValue": "INSUFFICIENT_DATA",
        "OKActions": [],
        "AlarmActions": ["arn:aws:sns:eu-west-1:123456789000:dataplatform_dlq_alerts"],
        "InsufficientDataActions": [],
        "Trigger": {
            "MetricName": "ApproximateNumberOfMessagesVisible",
            "Namespace": "AWS/SQS",
            "StatisticType": "Statistic",
            "Statistic": "SUM",
            "Unit": None,
            "Dimensions": [{"value": "DatasetEventsDLQ.fifo", "name": "QueueName"}],
            "Period": 60,
            "EvaluationPeriods": 1,
            "ComparisonOperator": "GreaterThanOrEqualToThreshold",
            "Threshold": 1.0,
            "TreatMissingData": "missing",
            "EvaluateLowSampleCountPercentile": "",
        },
    }


@pytest.fixture
def state_machine_message():
    return {
        "AlarmName": "Dataplatform-PipelineError-dataplatform-pipeline-excel-to-csv",
        "AlarmDescription": None,
        "AWSAccountId": "123456",
        "NewStateValue": "ALARM",
        "NewStateReason": "Threshold Crossed: 1 datapoint [1.0 (08/01/21 11:39:00)] was greater than or equal to the threshold (1.0).",
        "StateChangeTime": "2021-01-08T11:40:43.578+0000",
        "Region": "EU (Ireland)",
        "AlarmArn": "arn:aws:cloudwatch:eu-west-1:123456789000:alarm:Dataplatform-PipelineError-dataplatform-pipeline-excel-to-csv",
        "OldStateValue": "OK",
        "Trigger": {
            "MetricName": "ExecutionsFailed",
            "Namespace": "AWS/States",
            "StatisticType": "Statistic",
            "Statistic": "SUM",
            "Unit": None,
            "Dimensions": [
                {
                    "value": "arn:aws:states:eu-west-1:123456789000:stateMachine:dataplatform-pipeline-excel-to-csv",
                    "name": "StateMachineArn",
                }
            ],
            "Period": 60,
            "EvaluationPeriods": 1,
            "ComparisonOperator": "GreaterThanOrEqualToThreshold",
            "Threshold": 1.0,
            "TreatMissingData": "- TreatMissingData:                    notBreaching",
            "EvaluateLowSampleCountPercentile": "",
        },
    }


@pytest.fixture
def unknown_namespace_message():
    return {
        "AlarmName": "My alarm name",
        "NewStateReason": "My new state reason",
        "StateChangeTime": "2020.01.01",
        "AWSAccountId": "123456",
        "AlarmArn": "arn:aws:cloudwatch:eu-west-1:123456789000:alarm:Dataplatform_LambdaError_s3-writer-is-latest-edition",
        "Trigger": {
            "MetricName": "Errors",
            "Namespace": "AWS/Kappa",
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


def _event(message):
    return {
        "Records": [{"EventSource": "aws:sns", "Sns": {"Message": json.dumps(message)}}]
    }


@pytest.fixture
def lambda_event(lambda_message):
    return _event(lambda_message)


@pytest.fixture
def sqs_event(sqs_message):
    return _event(sqs_message)


@pytest.fixture
def state_machine_event(state_machine_message):
    return _event(state_machine_message)


@pytest.fixture
def unknown_namespace_event(unknown_namespace_message):
    return _event(unknown_namespace_message)
