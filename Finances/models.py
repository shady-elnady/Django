from django.db import models
from GraphQL.models import BaseModelNative

# Create your models here.


class Currency(BaseModelNative):
    code = models.CharField(max_length=5, blank=True, null=True, unique=True)
    emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)
