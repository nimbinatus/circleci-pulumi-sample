FROM python:3.9-slim

LABEL org.opencontainers.image.authors="Laura Santamaria laura@nimbinatus.com"

ENV PYTHONUNBUFFERED True

ENV APP_HOME /api
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:application