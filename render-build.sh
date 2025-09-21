#!/usr/bin/env bash
set -o errexit
set -o nounset
set -o pipefail

# Update system packages
apt-get update -y

# Install prerequisites
apt-get install -y curl apt-transport-https gnupg2 unixodbc-dev

# Add Microsoft package repo dynamically (detect distro codename)
DISTRO=$(lsb_release -cs || echo "bullseye")
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/$DISTRO/prod.list \
  > /etc/apt/sources.list.d/mssql-release.list

# Update again after adding repo
apt-get update -y

# Install ODBC Driver 17 + tools
ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools

# Optional: add SQL tools to PATH
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Upgrade pip and install Python deps
pip install --upgrade pip --no-cache-dir
pip install pyodbc --no-cache-dir
pip install -r requirements.txt --no-cache-dir
