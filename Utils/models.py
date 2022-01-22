from django.db import models
from GraphQL.models import BaseModel, BaseModelName, BaseModelNative
# Create your models here.


class Currency(BaseModelNative):
  code = models.CharField(max_length=5, blank=True, null=True, unique=True)
  emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)


class MobileCompany(BaseModelName):
  code = models.CharField(max_length=5, blank=True, null=True, unique=True)
  emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)


class Language(BaseModelNative):
  rtl = models.BooleanField(default=False)
  symbol = models.CharField(max_length=4, unique=True)
  is_active = models.BooleanField(default=False)


class StageLife(BaseModelName):
  from_age = models.SmallIntegerField()
  to_age = models.SmallIntegerField()


class MaritalStatus(BaseModelName):
  emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)
  is_active = models.BooleanField(default=False)


class Job(BaseModelName):
  pass


class Gender(BaseModelName):
  emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)
  is_active = models.BooleanField(default=False)


class Title(BaseModelName):
  stage_life = models.ForeignKey(
    StageLife, related_name="titles", on_delete=models.CASCADE
  )
  gender = models.ForeignKey(Gender, related_name="titles", on_delete=models.CASCADE)
  job = models.ForeignKey(
    Job, related_name="titles", null=True, on_delete=models.CASCADE
  )

  class Meta:
    unique_together = (
      "stage_life",
      "job",
      "gender",
    )


class Continent(BaseModelName):
  code = models.CharField(max_length=5, blank=True, null=True, unique=True)


class Country(BaseModelNative):
  code = models.CharField(max_length=5, blank=True, null=True, unique=True)
  tel_code = models.CharField(max_length=5, blank=True, null=True, unique=True)
  emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)
  continent = models.ForeignKey(
    Continent, related_name="countries", on_delete=models.CASCADE
  )
  language = models.ForeignKey(
    Language, related_name="countries", on_delete=models.CASCADE
  )


class Governorate(BaseModelNative):
  tel_code = models.CharField(max_length=3, blank=True, null=True, unique=True)
  country = models.ForeignKey(
      Country, related_name="governorates", on_delete=models.CASCADE
  )


class City(BaseModelNative):
  governorate = models.ForeignKey(
      Governorate, related_name="cities", on_delete=models.CASCADE
  )


class Village(BaseModelNative):
  city = models.ForeignKey(City, related_name="villages", on_delete=models.CASCADE)


class Street(BaseModelNative):
  village = models.ForeignKey(
    Village, related_name="streets", on_delete=models.CASCADE
  )


class Address(BaseModelNative):
  street = models.ForeignKey(Street, related_name="address", on_delete=models.CASCADE)
  house = models.CharField(max_length=50)
  location = models.CharField(max_length=100) # add Lat and Lang for Google Maps

