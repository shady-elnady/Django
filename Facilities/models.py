from django.db import models
from Persons.models import Person, Pharmacist
from GraphQL.models import BaseModel, BaseModelLogo, BaseModelName
from polymorphic.models import PolymorphicModel

# Create your models here.


class Facility(PolymorphicModel, BaseModelLogo):  # منشاءت
    # address = models.ForeignKey(Address, on_delete=models.CASCADE)
    # telephone = models.ForeignKey(Address, on_delete=models.CASCADE)
    # mobile = models.ForeignKey(Address, on_delete=models.CASCADE)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)


# TODO
class Store(Facility):  # مخازن
    pass


# TODO
class Branch(BaseModelName, BaseModel):
    # address = models.OneToOneField(Address, on_delete=models.CASCADE)
    # telphone = models.OneToOneField(Telephone, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    # TODO
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


# TODO
class MobileNetWork(Facility):  # شركات محمول
    code = models.CharField(max_length=5, blank=True, null=True, unique=True)
    emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)


# TODO
class Compony(Facility):  # شركات
    pass


class ScientificCompany(Compony):  # شركات مستلزمات معامل
    pass


class PharmaceuticalCompany(Compony):  # شركات أدويه
    pass


# TODO
class MedicalFacility(Facility):  # منشأه طبيه
    technical_supervisor = models.ForeignKey(Pharmacist, on_delete=models.CASCADE)


class Pharmacy(MedicalFacility):  # صيدليات
    pass


class Clinic(MedicalFacility):  # عيادات
    pass


class DentalClinic(Clinic):  # عيادات اسنان
    pass


class PrivateClinic(Clinic):  # هيادات خاصه
    pass


class Dispensary(MedicalFacility):  #  المستوصفات
    pass


# TODO
class Shop(Facility):  # محل
    pass


class Butcher(Shop):  # جزاره
    pass


class Grocery(Shop):  # بقاله
    pass


class Barber(Shop):  # محل حلاقه
    pass


# TODO
class Associations(Facility):  # الجمعيات
    pass
