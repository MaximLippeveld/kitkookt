FROM node:latest

ENV PYTHONUNBUFFERED TRUE

RUN apt-get update
RUN apt-get install -y git gcc python3-pip

ENV APP_HOME /app
WORKDIR ${APP_HOME}

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . ./

ENV DEBUG TRUE
RUN python3 manage.py tailwind build
RUN python3 manage.py collectstatic

CMD ["./scripts/entrypoint.sh"]