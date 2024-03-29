#!/bin/bash

# Importing .env source and config
source .env
set -e

echo " ------------------------------------ "
echo "|                                    |"
echo "|    Program Registered As User      |"
echo "|                                    |"
echo " ------------------------------------ "

# Send pull request
git stash
git pull https://$GITHUB_PASSWORD:x-oauth-basic@github.com/Razortype/django-homework-system.git
git stash pop

echo " ------------------------------------ "
echo "|                                    |"
echo "|   Github Data Fetching Complete    |"
echo "|                                    |"
echo " ------------------------------------ "

# Restart running services
echo $SYSTEM_USER_PASSWORD | sudo -S systemctl restart gunicorn
echo $SYSTEM_USER_PASSWORD | sudo -S systemctl restart nginx
echo $SYSTEM_USER_PASSWORD | sudo -S nginx -t

echo " ------------------------------------ "
echo "|                                    |"
echo "|    System Rebooted Successfully    |"
echo "|                                    |"
echo " ------------------------------------ "
