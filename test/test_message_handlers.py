import pytest

from slack.message_handlers import LambdaHandler, StateMachineHandler


def test_lambda_handler_slack_text(lambda_message):
    handler = LambdaHandler(lambda_message)
    text = handler.slack_text()

    assert "s3-writer-dev-is-latest-edition" in text
    assert "eu-west-1" in text
    assert "Monitoring" in text


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

    assert "State machine" in text
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
