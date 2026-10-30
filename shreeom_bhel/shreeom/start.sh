#!/usr/bin/env bash
exec gunicorn shreeom.wsgi:application
