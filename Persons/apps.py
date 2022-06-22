from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PersonsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Persons"
    verbose_name = _("Persons")

    def ready(self):
        import Persons.signals
