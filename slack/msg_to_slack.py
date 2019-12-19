import json
import requests

def lambda_handler(event, context):
    print(event)

    slack_data =  f"{event['message']} - Dato: {event['dato']}"

    webhook_url = 'https://hooks.slack.com/services/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'
   
    response = requests.post(
        webhook_url, json={"text": slack_data},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s' % (response.status_code, response.text)
    )
