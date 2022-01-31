from django.db import models
from GraphQL.models import BaseModelNative
# Create your models here.


class Language(BaseModelNative):
  rtl = models.BooleanField(default=False)
  symbol = models.CharField(max_length=4, unique=True)
  is_active = models.BooleanField(default=False)


