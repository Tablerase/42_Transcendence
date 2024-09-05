#!/bin/bash

# Alertmanager setup

# Get the secret Slack webhook URL
slack_webhook=$(cat $SLACK_WEBHOOK_URL_FILE)
# Copy the alertmanager config file
cp /tmp/config.yml /etc/alertmanager/config.yml

# Edit the alertmanager config file
sed -i "s|slack_api_url: <slack_webhook_url>|slack_api_url: '$slack_webhook'|g" /etc/alertmanager/config.yml

# Start the alertmanager service
/bin/alertmanager --config.file=/etc/alertmanager/config.yml --storage.path=/alertmanager
