#!/usr/bin/env bashio

export CONFIG_PATH=/data/options.json
export CL_API_KEY="$(bashio::config 'cl_api_key')"
export CL_API_SECRET="$(bashio::config 'cl_api_secret')"
export DJANGO_SECRET_KEY="$(bashio::config 'django_secret_key')"
export DEBUG="$(bashio::config 'debug')"

python manage.py migrate --no-input
python manage.py tailwind build --no-input
python manage.py collectstatic --no-input

chown -R nginx:nginx /app/static

nginx

/usr/local/bin/gunicorn kitkookt.wsgi:application \
--bind "127.0.0.1:7000" \
--error-logfile /data/error.log \
--access-logfile /data/access.log \
--env DJANGO_SETTINGS_MODULE=kitkookt.settings.production \
--env CL_API_KEY=$CL_API_KEY \
--env CL_API_SECRET=$CL_API_SECRET \
--env DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
--env DEBUG=$DEBUG
