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
IP_ADDRESS=$(grep -oP 'IP_ADDRESS=\K.*' $ENV_FILE)

# Replace the placeholder in the Nginx configuration template with the IP address
sed "s/{{IP_ADDRESS}}/$IP_ADDRESS/g" $NGINX_CONF_TEMPLATE > $NGINX_CONF_OUTPUT

systemctl reload nginx
