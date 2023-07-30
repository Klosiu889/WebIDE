# Web Integrated Development Environment

![Tests](https://github.com/Klosiu889/WebIDE/actions/workflows/test.yml/badge.svg?event=push)
![Lint](https://github.com/Klosiu889/WebIDE/actions/workflows/lint.yml/badge.svg?event=push)
[![Docker Pulls](https://badgen.net/docker/pulls/klosiu889/django_web_ide?icon=docker&label=pulls)](https://hub.docker.com/r/klosiu889/django_web_ide/)
[![codecov](https://codecov.io/gh/Klosiu889/WebIDE/branch/main/graph/badge.svg?token=ASQBPQTT2G)](https://codecov.io/gh/Klosiu889/WebIDE)

A university project to make simple website allowing file management and compilation of C programs.

## About

This simple website is build using django framework. It enables creating users and managing files by them.
For every user home directory is created when first logged in. User can create and delete files and
directories. Files can be edited and downloaded. Additionally website provides option to
compile files with sdcc compiler to assembly code.

## Build

Project requires python, nodejs and sdcc compiler to work.

First you will need to prepare python environment by installing packages:

```shell
pip install -r requirements.txt
```

Next go to Backend directory and with manage.py file run these commands to prepare database:
```shell
python manage.py makemigrations
python manage.py migrate
```

Alternatively you can download docker image with build app from this [repository](https://hub.docker.com/repository/docker/klosiu889/django_web_ide/general).

## Usage

To run server use inside Backend directory:
```shell
python manage.py runserver
```

And to run tests:
```shell
python manage.py test
```

Docker container starts django server by automatically.

## Actions

On every push three github actions are performed:

1. Running tests with coverage and upload]ing them to [Codecov](https://app.codecov.io/gh/Klosiu889/WebIDE).
2. Building docker image and uploading them to [dockerhub](https://hub.docker.com/r/klosiu889/django_web_ide/).
3. Running linting job using [Black github action](https://github.com/rickstaa/action-black).
