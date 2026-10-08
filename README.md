# sns-to-slack

Send SNS messages to Slack.

## Deploy

The service is defined in `template.yaml` and deployed with the [AWS SAM
CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
Per-environment settings (stack name, deployment bucket, region) live in
`samconfig.toml`.

Deploy to both dev and prod is automatic via GitHub Actions. You can
alternatively deploy from local machine with: `make deploy` or `make
deploy-prod`. This requires the SAM CLI and a local `python3.13` interpreter.
If you don't have Python 3.13, build inside Docker with `sam build
--use-container` instead.

The GitHub deploy role can only update an existing stack: it is not allowed to
create IAM roles or SNS subscriptions. The first deployment to an environment
must therefore be done from a local machine with administrator access.

## Slack integration

Messages are sent to Slack via webhooks. Webhooks are managed by Slack apps at
https://api.slack.com/apps.
