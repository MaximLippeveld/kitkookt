#!/bin/bash

CONFIG_PATH=/data/options.json
CL_API_KEY="$(bashio::config 'cl_api_key')"
CL_API_SECRET="$(bashio::config 'cl_api_secret')"

nginx

/usr/local/bin/gunicorn kitkookt.wsgi:application --bind "127.0.0.1:7000" --error-logfile /data/error.log --access-logfile /data/access.log --env DJANGO_SETTINGS_MODULE=kitkookt.settings.production --env CL_API_KEY=$CL_API_KEY --env CL_API_SECRET=$CL_API_SECRET
