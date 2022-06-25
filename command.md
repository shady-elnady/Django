python3 -m venv venv
python3 -m virtualenv -p python3.10 venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install django
django-admin startproject Config .
pip3 install python-decouple

# Apps
python3 manage.py startapp GraphQL
python3 manage.py startapp Persons
python3 manage.py startapp Products
python3 manage.py startapp Nady_System
python3 manage.py startapp Libraries
python3 manage.py startapp Utils

# Libraries
pip3 install djongo
pip3 install django-mongoengine
pip3 install django-polymorphic-tree
pip3 install gunicorn
pip3 install Pillow
pip3 install dnspython
pip3 install graphene-django
pip3 install django-filter
pip3 install django-graphql-jwt
pip3 install django-import-export
pip3 install django-debug-toolbar
pip3 install graphene-file-upload
pip3 install graphene-django-optimizer
pip3 install django-bootstrap-v5
pip3 install django-languages-plus
<!-- pip3 install django-countries -->
pip3 install django-allauth
pip3 install django-crispy-forms
pip3 install django-prices
pip3 install django-measurement
pip3 install django-pint
pip3 install django-cities
pip3 install django-currencies
pip3 install django-timezone-field
pip3 install django-spaghetti-and-meatballs
pip3 install django-countries-plus
pip3 install django-languages-plus
pip3 install django-currencies
pip3 install django-prices
pip3 install django-crispy-forms
pip3 install django-allauth
pip3 install django-timezone-field

# Commands
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
pip3 freeze
pip3 freeze > requirements.txt
deactivate

    - Languages
        python manage.py makemessages -l en
        python manage.py makemessages -l ar
        python manage.py compilemessages

        python manage.py loaddata languages_data.json.gz

pip3 install -r requirements.txt

# fixtures
python manage.py loaddata Persons