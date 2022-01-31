from django.db import models
from GraphQL.models import BaseModelName
from Persons.models import Person

# Create your models here.


class Specialization(BaseModelName):
  pass


class Doctor(Person):
  specialization = models.CharField(max_length=50 )
