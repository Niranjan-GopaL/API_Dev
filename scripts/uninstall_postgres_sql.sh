#!/bin/bash

# NOTE : this is to be done only in Ubutnu

# ee a list of packages related to PostgreSQL
dpkg -l | grep postgresql


# Disabling PostgreSQL Services
sudo systemctl disable postgresql


# Removing PostgreSQL Packages
sudo apt-get purge postgresql-16

#  Removing PostgreSQL Dependencies : command will remove any unused dependencies, including those related to PostgreSQL.
sudo apt-get autoremove

# Removing PostgreSQL Configuration Files
sudo rm -rf /etc/postgresql


# Removing PostgreSQL Data Directory
sudo rm -rf /var/lib/postgresql


sudo dpkg --purge postgresql-client-common postgresql-common

# Verifying Successful Uninstallation
dpkg -l | grep postgresql