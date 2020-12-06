#!/bin/bash

/usr/local/bin/gunicorn kitkookt.wsgi:application --bind "0.0.0.0:$PORT" --env DJANGO_SETTINGS_MODULE=kitkookt.settings.production