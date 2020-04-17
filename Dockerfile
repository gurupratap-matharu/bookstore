# pull base image
FROM python:3.7

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work dir
WORKDIR /code

# install requirements
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system --python 3.7

# copy project
COPY . /code/
