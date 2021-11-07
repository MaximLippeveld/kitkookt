ARG BUILD_FROM

FROM $BUILD_FROM

RUN apk add --update \
nodejs npm git build-base \
tiff-dev jpeg-dev openjpeg-dev zlib-dev \
nginx libxml2-dev libxslt-dev

ENV APP_HOME /app
WORKDIR ${APP_HOME}

RUN echo 'manylinux1_compatible = True' > /usr/local/lib/python3.9/site-packages/_manylinux.py
RUN python -c 'import sys; sys.path.append(r"/_manylinux.py")'

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

COPY kitkookt.conf /etc/nginx/http.d/

EXPOSE 7001

RUN chmod a+x run.sh
CMD ["/app/run.sh"]
