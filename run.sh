#!/bin/bash

nginx

/usr/local/bin/gunicorn kitkookt.wsgi:application --bind "127.0.0.1:7000" --error-logfile /data/error.log --access-logfile /data/access.log --env DJANGO_SETTINGS_MODULE=kitkookt.settings.production
