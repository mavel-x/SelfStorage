#!/bin/bash

set -e

if [ "$EUID" -ne 0 ]
  then
    echo "Please run as root."
    exit
fi

git pull
venv/bin/pip install -U -r requirements.txt
venv/bin/python manage.py collectstatic --noinput
venv/bin/python manage.py makemigrations --noinput
venv/bin/python manage.py migrate --noinput
systemctl restart selfstorage_django.service
systemctl reload nginx

echo "Project updated."
