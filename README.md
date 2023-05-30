# Web Integrated Development Environment
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
