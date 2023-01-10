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
git pull origin master <<EOF
$GITHUB_USERNAME
$GITHUB_PASSWORD
EOF

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
