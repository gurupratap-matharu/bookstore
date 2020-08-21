# pull base image
FROM python:3.7.2-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libpq-dev gcc
RUN /usr/local/bin/python -m pip install --upgrade pip

# set work dir
WORKDIR /code

# install requirements
COPY Pipfile Pipfile.lock /code/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system

# copy project
COPY . /code/
