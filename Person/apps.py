from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PersonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Person'
    verbose_name = _("Person")

    def ready(self):
        import Person.signals


