from django.db import models
from GraphQL.models import BaseModel, BaseModelName, BaseModelNative
from Utils.models import Country, Address

# Create your models here.


class Brand(BaseModelName):
  made_in = models.ForeignKey(Country, related_name='brands', on_delete=models.CASCADE)
  logo_url = models.CharField(max_length=100, null=True, blank=True)
      
      
class Product(BaseModelName):
  serial = models.CharField(max_length=50, unique=True)
  brand = models.ForeignKey(Brand, related_name="products", on_delete=models.CASCADE)
  volume = models.PositiveSmallIntegerField()