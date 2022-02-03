from django.db import models
from GraphQL.models import BaseModelNative
from Languages.models import Language

# Create your models here.



class Country(BaseModelNative):
  class Continent(models.TextChoices):
    Africa = 'AF'
    Antarctica = 'AN'
    Asia = 'AS'
    Europe = 'EU'
    NorthAmerica = 'NA'
    Oceania = 'OC'
    SouthAmerica = 'SA'
  code = models.CharField(max_length=5, blank=True, null=True, unique=True)
  tel_code = models.CharField(max_length=5, blank=True, null=True, unique=True)
  emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)
  continent = models.CharField(max_length=10, choices= Continent.choices)
  language = models.ForeignKey(
    Language, on_delete=models.CASCADE,
  )


class Governorate(BaseModelNative):
  tel_code = models.CharField(max_length=3, blank=True, null=True, unique=True)
  country = models.ForeignKey(
      Country, on_delete=models.CASCADE,
  )


class City(BaseModelNative):
  governorate = models.ForeignKey(
      Governorate, on_delete=models.CASCADE,
  )


class Village(BaseModelNative):
  city = models.ForeignKey(City, on_delete=models.CASCADE)


class Street(BaseModelNative):
  village = models.ForeignKey(
    Village, on_delete=models.CASCADE,
  )


class Address(BaseModelNative):
  street = models.ForeignKey(Street, on_delete=models.CASCADE)
  house = models.CharField(max_length=50)
  # TODO Location Google Maps
  location = models.CharField(max_length=100) # add Lat and Lang for Google Maps
