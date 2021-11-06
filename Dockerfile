ARG BUILD_FROM

FROM $BUILD_FROM

RUN apk add --update \
nodejs npm git build-base \
tiff-dev jpeg-dev openjpeg-dev zlib-dev \
nginx libxml2-dev libxslt-dev

ENV APP_HOME /app
WORKDIR ${APP_HOME}

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

ENV DJANGO_SETTINGS_MODULE kitkookt.settings.production

RUN python manage.py migrate --no-input
RUN python manage.py tailwind build --no-input
RUN python manage.py collectstatic --no-input

COPY kitkookt.conf /etc/nginx/http.d/

EXPOSE 7001

RUN chown -R nginx:nginx /app/static

RUN chmod a+x run.sh
CMD ["/app/run.sh"]
