import os

import pytest
from freezegun import freeze_time

from slack.message_handlers import LambdaHandler, StateMachineHandler


@freeze_time("2020-01-01T12:00:00+00:00")
def test_lambda_handler_kibana_url(lambda_message):
    handler = LambdaHandler(lambda_message)
    assert (
        handler.kibana_url("my_fun")
        == "http://localhost:8080/_plugin/kibana/app/discover#/?_a=(filters:!((query:(match_phrase:(function_name:my_fun))),(query:(match_phrase:(level:error)))))&_g=(time:(from:'2020-01-01T11:45:00Z',to:'2020-01-01T12:05:00Z'))"
    )


def test_lambda_handler_slack_text(lambda_message):
    handler = LambdaHandler(lambda_message)
    text = handler.slack_text()

    assert "s3-writer-dev-is-latest-edition" in text
    assert "eu-west-1" in text
    assert "Monitoring" in text
    assert os.environ["KIBANA_BASE_URL"] in text
    assert "Kibana" in text


def test_lambda_handler_slack_text_function_name_not_found(lambda_message):
    lambda_message["Trigger"]["Dimensions"] = [
        {"name": "TheFourth", "value": "lorem-ipsum"}
    ]
    handler = LambdaHandler(lambda_message)
    with pytest.raises(ValueError):
        handler.slack_text()


def test_state_machine_handler_slack_text(state_machine_message):
    handler = StateMachineHandler(state_machine_message)
    text = handler.slack_text()

    assert "Pipeline" in text
    assert "dataplatform-pipeline-excel-to-csv" in text
    assert "failed" in text


def test_state_machine_handler_slack_text_state_machine_arn_not_found(
    state_machine_message,
):
    state_machine_message["Trigger"]["Dimensions"] = [
        {"name": "TheFourth", "value": "lorem-ipsum"}
    ]
    handler = StateMachineHandler(state_machine_message)
    with pytest.raises(ValueError):
        handler.slack_text()
