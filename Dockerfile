FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app
RUN python -m pip install -r requirements.txt



