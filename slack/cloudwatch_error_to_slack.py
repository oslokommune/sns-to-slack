import os
import json
import requests

WEBHOOK_URL = os.environ["SLACK_ALERTS_WEBHOOK_URL"]

def handler(event, context):
    for record in event["Records"]:
        source = record['EventSource']
        if source != "aws:sns":
            raise ValueError(
                "Unsuported 'EventSource' %s. Supported types: 'aws:sns'"
                % (source)
            )

        sns = record["Sns"]
        message = json.loads(sns["Message"])

        try:
            # Assumed format: "arn:aws:cloudwatch:eu-west-1:***REMOVED***:alarm:ALARM_NAME"
            region = message["AlarmArn"].split(":")[3]
        except IndexError:
            region = "eu-west-1"

        prefix = "Dataplatform_LambdaError_"
        function_name = (
            message["AlarmName"].split(prefix, 1)
            if prefix in message["AlarmName"]
            else message["AlarmName"]
        )

        trigger = message["Trigger"]
        if trigger["Namespace"] == "AWS/Lambda":
            for dim in trigger["Dimensions"]:
                if dim["name"] == "FunctionName":
                    function_name = dim["value"]
                    break

        monitor_url = f"https://{region}.console.aws.amazon.com/lambda/home?region={region}#/functions/{function_name}?tab=monitoring"

        slack_data = (
            f"Lambda function *{function_name}* failed.\n"
            f"Reason: {message['NewStateReason']}\n"
            f"<{monitor_url}|Monitoring>\n"
        )

        response = requests.post(
            WEBHOOK_URL,
            json={
                "text": slack_data,
            },
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            raise ValueError(
                "Request to slack returned an error %s, the response is:\n%s"
                % (response.status_code, response.text)
            )
    return True
