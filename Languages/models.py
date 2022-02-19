from django.db import models
from django.utils.text import slugify
from GraphQL.models import BaseModelNative
from languages_plus.models import Language as _lang
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Language(BaseModelNative):
    iso_639_1 = models.CharField(
        max_length=2,
        unique=True,
        verbose_name=_("ISO 639-1"),
    )
    rtl = models.BooleanField(
        default=False,
        verbose_name=_("RtL"),
    )
    is_active = models.BooleanField(default=False)

    @property
    def slug(self):
        return slugify(self.code)

    @property
    def langObj(self):
        return _lang.objects.get(iso_639_1=self.iso_639_1)
        """_summary_
            name_en (ISO Language Name)
            name_native (Native Name)
            iso_639_1 (639-1)
            iso_639_2T = (639-2/T)
            iso_639_2B = (639-2/B)
            iso_639_3 = (639-3)
            family = (Language Family)
            countries_spoken
        """

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
