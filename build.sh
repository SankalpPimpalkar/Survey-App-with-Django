#!/bin/bash
echo "Python version:"
python3 --version

echo "Installing dependencies..."
pip install -r requirements.txt

python3 manage.py collectstatic --noinput
python3 manage.py tailwind build
