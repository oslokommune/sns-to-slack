# Send messages and alerts to Slack

* **cloudwatch_error_to_slack**: Sends errors from Lambda and state machine
  executions to Slack.

## Deploy

Deploy to dev is automatic via GitHub Actions, while deploy to prod can be triggered with GitHub Actions via dispatch. You can alternatively deploy from local machine (requires `saml2aws`) with: `make deploy` or `make deploy-prod`.
