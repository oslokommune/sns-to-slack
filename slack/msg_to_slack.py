import json
import requests

def handler(event, context):
    params = event["pathParameters"]
    slack_data = params["slack"]

    webhook_url = '***REMOVED***'

    data = json.dumps(slack_data)
    response = requests.post(
        webhook_url, json={"text": data},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )
