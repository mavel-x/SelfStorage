#!/bin/bash

set -e

if [ "$EUID" -ne 0 ]; then
  echo "Please run this as root."
  exit 1
fi

# Install Docker
apt-get update
apt-get install -y ca-certificates curl gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --yes --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

apt-get install -y nginx

python3 -m venv ./venv
./venv/bin/pip install -r requirements.txt

./venv/bin/python manage.py collectstatic --noinput
./scripts/init_postgres.sh
./scripts/init_systemd_units.sh
./scripts/init_nginx.sh
