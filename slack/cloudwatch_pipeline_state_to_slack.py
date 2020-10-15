import requests
from env import WEBHOOK_URL


def check_if_status_is_failed(details):
    status = details.get("status")
    failed_statuses = [
        "ABORTED",
        "FAILED",
        "TIMED_OUT"
    ]

    return status in failed_statuses


def get_slack_text(details):
    pipeline_id = details.get("name")
    status = details.get("status")
    return (
        f"Pipeline with id: {pipeline_id} failed.\n"
        f"Status is: {status}"
    )


def handler(event, context):
    details = event.get("detail", None)
    if not details:
        return False

    if check_if_status_is_failed(details):
        response = requests.post(
            WEBHOOK_URL,
            json={
                "text": get_slack_text(details)
            },
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            raise ValueError(
                "Request to slack returned an error %s, the response is:\n%s"
                % (response.status_code, response.text)
            )

    return True
