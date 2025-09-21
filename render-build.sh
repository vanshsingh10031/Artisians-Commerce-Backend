#!/usr/bin/env bash

set -e  # stop on error

# Update system
apt-get update -y
apt-get install -y curl gnupg2 software-properties-common apt-transport-https

# Add Microsoft repo for ODBC drivers (Debian 11 = bullseye)
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install ODBC Driver 17 and unixODBC
apt-get update -y
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# Upgrade pip & install Python deps
pip install --upgrade pip --no-cache-dir
pip install pyodbc --no-cache-dir
pip install -r requirements.txt --no-cache-dir
