import os

import requests


class BaseHandler:
    webhook_url: str = None

    def __init__(self, msg):
        self.region = self._message_region(msg)
        self.dimensions = {d["name"]: d["value"] for d in msg["Trigger"]["Dimensions"]}

    def _message_region(self, message):
        try:
            # Assumed format: "arn:aws:cloudwatch:eu-west-1:xxxxxxxxxxxx:alarm:ALARM_NAME"
            return message["AlarmArn"].split(":")[3]
        except (KeyError, IndexError):
            return "eu-west-1"

    def aws_base_url(self, service):
        return f"https://{self.region}.console.aws.amazon.com/{service}/home?region={self.region}#"

    def slack_text(self):
        raise NotImplementedError

    def post_to_slack(self):
        response = requests.post(
            self.webhook_url,
            json={"text": self.slack_text()},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            raise ValueError(
                "Request to Slack gave an error code {}, the response is:\n{}".format(
                    response.status_code, response.text
                )
            )


class LambdaHandler(BaseHandler):
    webhook_url = os.environ["SLACK_LAMBDA_ALERTS_WEBHOOK_URL"]
    msg_format = os.environ["SLACK_LAMBDA_ALERTS_MSG_FORMAT"]

    def slack_text(self):
        function_name = self.dimensions.get("FunctionName")

        if not function_name:
            raise ValueError("Lambda function name not found")

        base_url = self.aws_base_url("lambda")

        return self.msg_format.format(
            config_url=f"{base_url}/functions/{function_name}?tab=configuration",
            function_name=function_name,
            monitor_url=f"{base_url}/functions/{function_name}?tab=monitoring",
        )


class StateMachineHandler(BaseHandler):
    webhook_url = os.environ["SLACK_STATE_MACHINE_ALERTS_WEBHOOK_URL"]
    msg_format = os.environ["SLACK_STATE_MACHINE_ALERTS_MSG_FORMAT"]

    def slack_text(self):
        state_machine_arn = self.dimensions.get("StateMachineArn")

        if not state_machine_arn:
            raise ValueError("State machine ARN not found")

        base_url = self.aws_base_url("states")

        return self.msg_format.format(
            url=f"{base_url}/statemachines/view/{state_machine_arn}",
            name=state_machine_arn.split(":")[-1],
        )
