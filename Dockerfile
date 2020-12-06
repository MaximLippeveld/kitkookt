FROM python:3.8.2-slim

ENV PYTHONUNBUFFERED TRUE

RUN apt-get update
RUN apt-get install -y git gcc
RUN pip install --upgrade pip

ENV APP_HOME /app
WORKDIR ${APP_HOME}

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

CMD ["./scripts/entrypoint.sh"]