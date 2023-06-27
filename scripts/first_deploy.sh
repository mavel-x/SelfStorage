#!/bin/bash

set -e

if [ "$EUID" -ne 0 ]; then
  echo "Please run this as root."
  exit 1
fi

# Install Docker
apt-get update
apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io

apt-get install -y nginx

python3 -m venv ./venv
./venv/bin/pip install -r requirements.txt

./venv/bin/python manage.py collectstatic --noinput
./scripts/init_postgres.sh
./scripts/init_systemd_units.sh
./scripts/init_nginx.sh
