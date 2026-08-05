# sns-to-slack

Send SNS messages to Slack.

## Deploy

Deploy to both dev and prod is automatic via GitHub Actions. You can
alternatively deploy from local machine with: `make deploy` or `make
deploy-prod`.

## Slack integration

Messages are sent to Slack via webhooks. Webhooks are managed by Slack apps at
https://api.slack.com/apps.
