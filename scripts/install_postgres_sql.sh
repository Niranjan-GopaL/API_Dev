#!/bin/bash

# Install necessary packages
sudo apt update
sudo apt install -y curl ca-certificates

# Create directory for PostgreSQL GPG key
sudo install -d /usr/share/postgresql-common/pgdg

# Download and add PostgreSQL GPG key
sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc

# Add PostgreSQL APT repository
sudo sh -c 'echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Update package list and install PostgreSQL
sudo apt update
sudo apt -y install postgresql