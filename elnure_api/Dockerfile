FROM python:3.9-slim-buster
WORKDIR /elnure_api
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean
# install python dependencies
RUN pip install --upgrade pip
COPY ./Pipfile /elnure_api/Pipfile
RUN pip install pipenv
RUN pipenv install
COPY . /elnure_api/