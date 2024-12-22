#!/bin/bash
echo "Python version:"
python3 --version

python3 manage.py collectstatic --noinput
python3 manage.py tailwind build
