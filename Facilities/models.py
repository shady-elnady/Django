from django.db import models
from Persons.models import Person, Pharmacist
from GraphQL.models import  BaseModelLogo
from polymorphic.models import PolymorphicModel 

# Create your models here.

class Facility(PolymorphicModel, BaseModelLogo): # منشاءت
  # address = models.ForeignKey(Address, on_delete=models.CASCADE)
  # telephone = models.ForeignKey(Address, on_delete=models.CASCADE)
  # mobile = models.ForeignKey(Address, on_delete=models.CASCADE)
  owner = models.ForeignKey(Person, on_delete=models.CASCADE)


# TODO  NOTES
class Compony(Facility): # شركات
  pass


class MobileCompany(Compony):
    code = models.CharField(max_length=5, blank=True, null=True, unique=True)
    emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)



# TODO  NOTES
class Laboratory(Facility):
    pass


class MainLab(Laboratory):
    pass


class Lab(Laboratory):
    pass

  
class Pharmacy(Facility): # صيدليات
  technical_supervisor = models.ForeignKey(Pharmacist, on_delete=models.CASCADE)


# TODO  NOTES



class Clinic(Facility): # عيادات 
  pass

class DentalClinic(Clinic): # عيادات اسنان
  pass


class PrivateClinic(Clinic): # هيادات خاصه
  pass


# TODO  NOTES

class Shop(Facility): # محل
  pass


class Butcher(Shop): # جزاره
  pass


class Grocery(Shop): # بقاله
  pass


class Barber(Shop): # محل حلاقه
  pass

# TODO  NOTES

class Store(Facility): # مخازن
  pass


# TODO  NOTES

class DispensaryAssociations(Facility): # الجمعيات - المستوصفات
  pass
