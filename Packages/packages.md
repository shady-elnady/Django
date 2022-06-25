django-spaghetti-and-meatballs
https://django-spaghetti-and-meatballs.readthedocs.io/en/latest/


# django-languages-plus
python manage.py migrate
python manage.py loaddata languages_data.json.gz
with django-countries-plus :
  from languages_plus.utils import associate_countries_and_languages
  associate_countries_and_languages()

# django-currencies
python3 manage.py migrate currencies 0001 --fake
python3 manage.py currencies -i SHOP_CURRENCIES
python3 manage.py updatecurrencies oxr --base=USD

# django-countries-plus
python3 manage.py update_countries_plus

(alternative) Load the provided fixture from the fixtures directory.
  python manage.py loaddata PATH_TO_COUNTRIES_PLUS/countries_plus/countries_data.json.gz

with django-languages-plus :
  from languages_plus.utils import associate_countries_and_languages
  associate_countries_and_languages()