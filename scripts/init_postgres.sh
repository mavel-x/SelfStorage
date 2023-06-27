#!/bin/bash

if [ "$EUID" -ne 0 ]
  then
    echo "Please run as root."
    exit
fi

if [ $( docker ps -a | grep selfstorage-postgres | wc -l ) -gt 0 ]
  then
    echo "Postgres container already exists."
    exit
fi

apt-get install libpq-dev

docker run -d --name selfstorage-postgres \
--env-file .env -p 5432:5432 \
-v selfstorage_postgres:/var/lib/postgresql/data \
postgres:14
sleep 1
venv/bin/python ./manage.py migrate --noinput
venv/bin/python manage.py upload_test_data
docker stop -t 10 selfstorage-postgres
