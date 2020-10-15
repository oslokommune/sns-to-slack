import json

import requests
from env import WEBHOOK_URL


def slackTextFromSnsMessage(message):
    trigger = message["Trigger"]
    if trigger["Namespace"] != "AWS/Lambda":
        raise ValueError(
            "Unsuported SNS message trigger namespace' %s. Supported types: 'AWS/Lambda'"
            % (trigger["Namespace"])
        )

    try:
        # Assumed format: "arn:aws:cloudwatch:eu-west-1:***REMOVED***:alarm:ALARM_NAME"
        region = message["AlarmArn"].split(":")[3]
    except (KeyError, IndexError):
        region = "eu-west-1"

    function_name = None
    for dim in trigger["Dimensions"]:
        if dim["name"] == "FunctionName":
            function_name = dim["value"]
            break

    if function_name is None:
        raise ValueError("Lambda function name not found.")

    config_url = f"https://{region}.console.aws.amazon.com/lambda/home?region={region}#/functions/{function_name}?tab=configuration"
    monitor_url = f"https://{region}.console.aws.amazon.com/lambda/home?region={region}#/functions/{function_name}?tab=monitoring"

    return (
        f"Lambda function *<{config_url}|{function_name}>* failed.\n"
        f"<{monitor_url}|Monitoring>\n"
    )


def slackTextFromRecord(record):
    source = record["EventSource"]
    if source == "aws:sns":
        sns = record["Sns"]
        message = json.loads(sns["Message"])
        return slackTextFromSnsMessage(message)
    else:
        raise ValueError(
            "Unsuported 'EventSource' %s. Supported types: 'aws:sns'" % (source)
        )


def handler(event, context):
    for record in event["Records"]:
        slackText = slackTextFromRecord(record)

        response = requests.post(
            WEBHOOK_URL,
            json={
                "text": slackText,
            },
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            raise ValueError(
                "Request to slack returned an error %s, the response is:\n%s"
                % (response.status_code, response.text)
            )
    return True
