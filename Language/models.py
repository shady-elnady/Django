from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from languages_plus.models import Language as BaseLanguage
from GraphQL.models import BaseModel, BaseModelNative

# Create your models here.


class Language(BaseModel, BaseModelNative):

    rtl = models.BooleanField(
        default=False,
        verbose_name=_("RtL"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("is_Active"),
    )

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    @property
    def langInfo(self):
        return BaseLanguage.objects.get(name_en=self.name)
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
