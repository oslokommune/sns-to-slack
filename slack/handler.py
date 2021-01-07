import json

from slack.message_handlers import LambdaHandler, PipelineHandler

message_handlers = {
    "AWS/Lambda": LambdaHandler,
    "AWS/States": PipelineHandler,
}


def _record_message(record):
    """Return the message part of the given SNS record."""

    source = record["EventSource"]

    if source == "aws:sns":
        return json.loads(record["Sns"]["Message"])

    raise ValueError(f"Unsuported 'EventSource' {source}. Supported types: 'aws:sns'")


def cloudwatch_error_to_slack(event, context):
    for msg in map(_record_message, event["Records"]):
        ns = msg["Trigger"]["Namespace"]

        try:
            handler_cls = message_handlers[ns]
            handler = handler_cls(msg)
            handler.post_to_slack()
        except KeyError:
            raise ValueError(
                "Unsuported SNS message trigger namespace: {}. Supported types: {}".format(
                    ns, ", ".join(message_handlers.keys())
                )
            )

    return True
