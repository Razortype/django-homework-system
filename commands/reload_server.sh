#!/bin/bash

# Importing .env source and config
source .env
set -e

# Restart running services
echo $SYSTEM_USER_PASSWORD | sudo -S systemctl restart gunicorn
echo $SYSTEM_USER_PASSWORD | sudo -S systemctl restart nginx
echo $SYSTEM_USER_PASSWORD | sudo -S nginx -t

echo " ------------------------------------ "
echo "|                                    |"
echo "|    System Rebooted Successfully    |"
echo "|                                    |"
echo " ------------------------------------ "