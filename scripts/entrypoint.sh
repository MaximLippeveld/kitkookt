#!/bin/bash

/usr/local/bin/gunicorn kitkookt.wsgi:application --bind "0.0.0.0:$PORT" --error-logfile error.log --access-logfile access.log --env DJANGO_SETTINGS_MODULE=kitkookt.settings.production