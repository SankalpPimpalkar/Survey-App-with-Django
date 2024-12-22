#!/bin/bash
# Install dependencies
pip3 install -r requirements.txt

# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs

# Debugging: Check Node.js and npm versions
node --version
npm --version

# Set up Django
python3 manage.py collectstatic --noinput
python3 manage.py tailwind build
python3 manage.py migrate
