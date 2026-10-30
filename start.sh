#!/usr/bin/env bash
# Exit on error
set -o errexit

if [ -d "shreeom_bhel/shreeom" ]; then
    exec gunicorn --chdir shreeom_bhel/shreeom shreeom.wsgi:application
else
    exec gunicorn shreeom.wsgi:application
fi

