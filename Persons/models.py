from django.db import models
from GraphQL.models import BaseModel, BaseModelName, BaseModelNative
from Utils.models import Gender, Job, Title
from polymorphic.models import PolymorphicModel 
# Create your models here.


class Person(PolymorphicModel, BaseModel):
  national_id = models.SmallIntegerField(unique=True)
  full_name = models.CharField(max_length=50, unique=True)
  family_name = models.CharField(max_length=10)
  birth_date = models.DateField()
  image_url = models.ImageField(
      upload_to="images", editable=True, null=True, blank=True
  )
  gender = models.ForeignKey(
      Gender, on_delete=models.CASCADE, related_name="persons"
  )
  Job = models.ForeignKey(Job, on_delete=models.SET_NULL, related_name="persons", null=True, blank=True)
  title = models.ForeignKey(Title, on_delete=models.SET('Deleted FK'), related_name="persons", null=True, blank=True)
  

class Doctor(Person):
  pass


class Patient(Person):
  pass


class Customer(Person):
  pass


class Employee(Person):
  pass


class User(Person):
  pass