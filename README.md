Send message from Lambda too Slack
==================

Sends message and status to group Lambda-Meldinger on Slack

The message in Json-format:
* name:   lambdaname?
* status: FAILED? ERROR? WARNING?
* message:
* dato:

## Example
* **msg_to_slack** is the lambda-function that send the message to slack
* **lambda_to_slack** is an example of how to invoke the msg_to_slack
