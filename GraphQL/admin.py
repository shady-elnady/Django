from django.contrib import admin
from django.apps import apps

# Register your models here.


models = apps.get_models()


for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

# pip install django-easymode

# from easymode.i18n.admin.decorators import L10n
# from foobar.models import Foo

# admin.site.register(Foo, L10n(Foo, models.ModelAdmin))
