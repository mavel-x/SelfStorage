#!/bin/bash

set -e

if [ "$EUID" -ne 0 ]
  then
    echo "Please run as root."
    exit
fi

cd /opt/SelfStorage/

git pull
venv/bin/pip install -U -r requirements.txt
venv/bin/python manage.py collectstatic --noinput
venv/bin/python manage.py makemigrations --noinput
venv/bin/python manage.py migrate --noinput
systemctl daemon-reload
systemctl restart selfstorage.target
systemctl reload nginx

echo "Project updated."
