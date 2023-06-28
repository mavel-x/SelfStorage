#!/bin/bash

set -e

# Check if there are any files in the /etc/nginx/sites-enabled/ directory besides default
if [ $(ls /etc/nginx/sites-enabled/ | grep -v '^default$' | wc -l) -gt 0 ]; then
  echo "There are other sites configured in the /etc/nginx/sites-enabled/ directory. Exiting."
  exit 1
fi

cd /opt/SelfStorage/

ENV_FILE="./.env"
NGINX_CONF_TEMPLATE="./nginx.conf.template"
NGINX_CONF_OUTPUT="/etc/nginx/sites-enabled/selfstorage.conf"
SERVER_IP=$(grep -oP 'SERVER_IP=\K.*' $ENV_FILE)
SERVER_NAME=$(grep -oP 'SERVER_NAME=\K.*' $ENV_FILE)

# Replace the placeholders in the Nginx configuration template with the IP address and server name
sed "s/{{SERVER_IP}}/$SERVER_IP/g; s/{{SERVER_NAME}}/$SERVER_NAME/g" $NGINX_CONF_TEMPLATE > $NGINX_CONF_OUTPUT

systemctl reload nginx
