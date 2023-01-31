# Lab 32

## Author: Aubrey Corsetti

### How to run tests:

python manage.py runserver Navigate to snacks/tests 
Run in terminal: python manage.py test

Setup
> python3.11 -m venv .venv 
> pip install django 
> pip install djangorestframework
> pip install psycopg2-binary
> pip freeze > requirements.txt
> django-admin startproject jobs_project . 
> python manage.py startapp jobs 
> python manage.py createsuperuser 
> python manage.py makemigrations jobs 
> python manage.py migrate python manage.py runserver

Load the site at http://0.0.0.0:8001/admin