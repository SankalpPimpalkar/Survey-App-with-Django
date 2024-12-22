#!/bin/bash

# Install Python dependencies
pip3 install -r requirements.txt

# Install Node.js dependencies using npm
npm install

# Collect static files (important for Django's static files management)
python3 manage.py collectstatic --noinput

# Build Tailwind CSS
npm run build

# Apply database migrations
python3 manage.py migrate
