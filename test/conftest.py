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
def pipeline_message():
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


@pytest.fixture
def lambda_event(lambda_message):
    return {
        "Records": [
            {"EventSource": "aws:sns", "Sns": {"Message": json.dumps(lambda_message)}}
        ]
    }


@pytest.fixture
def pipeline_event(pipeline_message):
    return {
        "Records": [
            {"EventSource": "aws:sns", "Sns": {"Message": json.dumps(pipeline_message)}}
        ]
    }


@pytest.fixture
def unknown_namespace_event(unknown_namespace_message):
    return {
        "Records": [
            {
                "EventSource": "aws:sns",
                "Sns": {"Message": json.dumps(unknown_namespace_message)},
            }
        ]
    }
