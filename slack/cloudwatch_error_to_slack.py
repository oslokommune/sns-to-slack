import json
import requests

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

def lambda_handler(event, context):
    webhook_url = SLACK_WEBHOOK_URL
    for record in event["Records"]:
        sns = record["Sns"]
        message = json.loads(sns["Message"])
        slack_data = f"*Alarm:* {message['AlarmName']}\n *Reason:* {message['NewStateReason']}\n *At:* {message['StateChangeTime']}\n *Account:* {message['AWSAccountId']}\n"

        response = requests.post(
            webhook_url, json={"text": slack_data, "username": "LambdaError","icon_emoji":":ghost:"},
            headers={'Content-Type': 'application/json'}
        )

        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text)
        )
