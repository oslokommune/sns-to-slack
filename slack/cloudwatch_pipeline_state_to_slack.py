import json

import requests

from slack.env import WEBHOOK_URL


def check_if_status_is_failed(details):
    status = details.get("status")
    failed_statuses = ["ABORTED", "FAILED", "TIMED_OUT"]

    return status in failed_statuses


def get_slack_text(details, region):
    state_machine_arn = details.get("stateMachineArn")
    execution_arn = details.get("executionArn")

    state_machine_name = state_machine_arn.split(":")[-1]

    prefix = "dataplatform-"

    # When we get Lambda 3.9 support: replace with https://docs.python.org/3/library/stdtypes.html#str.removeprefix
    if state_machine_name.startswith(prefix):
        state_machine_name = state_machine_name[len(prefix) :]

    base_url = f"https://{region}.console.aws.amazon.com/states/home?region={region}#"

    state_machine_url = f"{base_url}/statemachines/view/{state_machine_arn}"
    execution_url = f"{base_url}/executions/details/{execution_arn}"

    status = details.get("status")
    return (
        f"Pipeline *<{state_machine_url}|{state_machine_name}>* failed with status: {status}\n"
        f"<{execution_url}|Execution details>"
    )


def handle_message(message):
    details = message.get("detail", None)
    if not details:
        return False

    if check_if_status_is_failed(details):
        region = message.get("region")
        response = requests.post(
            WEBHOOK_URL,
            json={"text": get_slack_text(details, region)},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            raise ValueError(
                f"Request to slack returned an error {response.status_code}, the response is:\n{response.text}"
            )

    return True


def handler(event, context):
    records = event.get("Records", None)
    if not records:
        raise ValueError("Event does not contain Records")
    record = records[0]
    source = record["EventSource"]
    if source == "aws:sns":
        sns = record["Sns"]
        event = json.loads(sns["Message"])
        return handle_message(event)
    else:
        raise ValueError(
            f"Unsuported 'EventSource' {source}. Supported types: 'aws:sns'"
        )
