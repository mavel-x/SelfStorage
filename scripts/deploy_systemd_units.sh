#!/bin/bash

set -e

cd /opt/SelfStorage/

cp ./systemd_units/* /etc/systemd/system/

systemctl daemon-reload
systemctl enable selfstorage.target
systemctl start selfstorage.target

echo "Started services and timers."
