#!/bin/bash

/usr/local/bin/gunicorn kitkookt.wsgi:application --bind "0.0.0.0:7000" --error-logfile /data/error.log --access-logfile /data/access.log --env DJANGO_SETTINGS_MODULE=kitkookt.settings.production