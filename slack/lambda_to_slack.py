import boto3
from datetime import datetime
import json

client = boto3.client('lambda')

def lambda_handler(event, context):
    arn = 'arn:aws:lambda:eu-west-1:***REMOVED***:function:lambda-boilerplate-dev-msg_to_slack'
    data = {
        'message': 'Message from lambda',
        'dato': datetime.now().isoformat()

            }
    
    response = client.invoke(FunctionName=arn,
                             InvocationType='RequestResponse',
                             Payload=json.dumps(data))

    result = json.loads(response.get('Payload').read())
    return result