#!/usr/bin/env bash

set -o errexit  # stop on error
set -o nounset  # stop on unbound variable
set -o pipefail # catch pipe fails

# Update system packages
apt-get update -y

# Install prerequisites
apt-get install -y curl apt-transport-https gnupg

# Add Microsoft package repo for ODBC driver
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Update again after adding repo
apt-get update -y

# Install ODBC Driver 17 for SQL Server + tools
ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools unixodbc-dev

# Optional: make sqlcmd and bcp globally available
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Upgrade pip + install Python deps
pip install --upgrade pip --no-cache-dir
pip install pyodbc --no-cache-dir
pip install -r requirements.txt --no-cache-dir
