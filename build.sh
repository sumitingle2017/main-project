#!/usr/bin/env bash
# Exit on error
set -o errexit

if [ -d "shreeom_bhel/shreeom" ]; then
    cd shreeom_bhel/shreeom
fi

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

