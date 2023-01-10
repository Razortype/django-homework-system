#!/bin/bash

# Importing .env source and config
source ../.env
set -e

# Check current user validation
echo $SYSTEM_USER_PASSWORD | sudo orkun

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
sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo nginx -t

echo " ------------------------------------ "
echo "|                                    |"
echo "|    System Rebooted Successfully    |"
echo "|                                    |"
echo " ------------------------------------ "