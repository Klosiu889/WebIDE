# Web Integrated Development Environment

![Tests](https://github.com/Klosiu889/WebIDE/actions/workflows/test.yml/badge.svg?event=push)
![Lint](https://github.com/Klosiu889/WebIDE/actions/workflows/lint.yml/badge.svg?event=push)
[![codecov](https://codecov.io/gh/Klosiu889/WebIDE/branch/main/graph/badge.svg?token=ASQBPQTT2G)](https://codecov.io/gh/Klosiu889/WebIDE)

A university project to make simple website allowing file management and comilation of C programs.

## Usage

First you will need to install required python packages:

```shell
pip install -r requirements.txt
```

Go to Backend directory with manage.py file run these commands to prepare database:
```shell
python manage.py makemigrations
python manage.py migrate
```
To run server use:
```shell
python manage.py runserver
```

And to run tests:
```shell
python manage.py test
```
