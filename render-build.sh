#!/usr/bin/env bash

# Update and install system dependencies for MSSQL
apt-get update -y
apt-get install -y freetds-dev freetds-bin unixodbc-dev

# Upgrade pip and install Python dependencies
pip install --upgrade pip --no-cache-dir
pip install pyodbc --no-cache-dir
pip install -r requirements.txt --no-cache-dir
