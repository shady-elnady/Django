python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip3 install django
pip3 install python-decouple
django-admin startproject Config .

python3 manage.py startapp GraphQL
python3 manage.py startapp Persons
python3 manage.py startapp Products
python3 manage.py startapp Libraries
python3 manage.py startapp Utils

pip3 install djongo
pip3 install django-mongoengine
pip3 install django-polymorphic-tree
pip3 install gunicorn

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
pip3 freeze
pip3 freeze > requirements.txt
deactivate

pip3 install -r requirements.txt