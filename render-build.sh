#!/usr/bin/env bash

# Install system dependencies for MSSQL
apt-get update
apt-get install -y freetds-dev freetds-bin unixodbc-dev

# Install Python dependencies
pip install --upgrade pip
pip install pyodbc
pip install -r requirements.txt
