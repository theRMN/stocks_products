#! /bin/bash

python manage.py migrate

python manage.py collectstatic

gunicorn stocks_products.wsgi -b 0.0.0.0:8000
