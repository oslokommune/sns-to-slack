import json

import requests

from slack.env import WEBHOOK_URL


def check_if_status_is_failed(details):
    status = details.get("status")
    failed_statuses = ["ABORTED", "FAILED", "TIMED_OUT"]

    return status in failed_statuses


def get_slack_text(details):
    pipeline_id = details.get("name")
    status = details.get("status")
    return f"Pipeline with id: {pipeline_id} failed.\n" f"Status is: {status}"


def handle_message(message):
    details = message.get("detail", None)
    if not details:
        return False

    if check_if_status_is_failed(details):
        response = requests.post(
            WEBHOOK_URL,
            json={"text": get_slack_text(details)},
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
