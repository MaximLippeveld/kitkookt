ARG BUILD_FROM

FROM $BUILD_FROM

RUN apk add --update \
nodejs npm git build-base \
tiff-dev jpeg-dev openjpeg-dev zlib-dev

ENV APP_HOME /app
WORKDIR ${APP_HOME}

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

RUN python manage.py migrate --no-input
RUN python manage.py tailwind build --no-input
RUN python manage.py collectstatic

RUN chmod a+x run.sh
CMD [ "/app/run.sh" ]
