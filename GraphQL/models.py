from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Create your models here.


class BaseModel(models.Model):
    create_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Craeted At"),
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=True,
        null=True,
        verbose_name=_("Last Update"),
    )

    class Meta:
        abstract = True


class BaseModelName(models.Model):
    name = models.CharField(
        max_length=50,
        primary_key=True,
        verbose_name=_("Name"),
    )

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class BaseModelNative(BaseModelName):
    native = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Native"),
    )

    class Meta:
        abstract = True


class BaseModelEmoji(BaseModelName):
    emoji = models.CharField(
        max_length=5,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Emoji"),
    )

    class Meta:
        abstract = True


class BaseModelLogo(BaseModelName):
    logo_img = models.ImageField(
        upload_to="images/logo/",
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("Logo IMG"),
    )

    class Meta:
        abstract = True
