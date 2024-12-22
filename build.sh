#!/bin/bash

# Install Python dependencies
pip3 install -r requirements.txt

# Install Node.js dependencies
npm install

# Collect static files for production
python3 manage.py collectstatic --noinput

# Build Tailwind CSS (This will run your npm scripts to generate the styles)
npm run build

# Apply database migrations (for Vercel deployment)
python3 manage.py migrate
