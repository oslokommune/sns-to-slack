# Send messages and alerts to Slack

* **cloudwatch_error_to_slack**: Sends errors from Lambda and state machine
  executions to Slack.

## Deploy

Deploy to dev is automatic via GitHub Actions, while deploy to prod can be triggered with GitHub Actions via dispatch. You can alternatively deploy from local machine (requires `saml2aws`) with: `make deploy` or `make deploy-prod`.

## Slack integration

Messages are sent to Slack via webhooks. Webhooks are managed as
legacy Incoming WebHooks at https://app.slack.com/apps-manage/ and as
Slack apps at https://api.slack.com/apps
