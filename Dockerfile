ARG BUILD_ARG

FROM ${BUILD_ARG}

RUN apk add --update nodejs npm

ENV APP_HOME /app
WORKDIR ${APP_HOME}

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . ./

RUN python3 manage.py tailwind build
RUN python3 manage.py collectstatic
