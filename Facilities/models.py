from django.db import models

# from djongo.models import ArrayReferenceField
# from Persons.models import Person, Pharmacist
from GraphQL.models import BaseModel, BaseModelLogo, BaseModelName
from polymorphic.models import PolymorphicModel

# Create your models here.


class Job(PolymorphicModel, BaseModelName):
    pass


class Facility(PolymorphicModel, BaseModelLogo):  # منشاءت
    # TODO ADRESS TELPHONE LOCATION
    owner = models.ForeignKey(to="Persons.Person", on_delete=models.CASCADE)


class Store(Facility):  # مخازن
    pass


class Branch(BaseModelName, BaseModel):
    # TODO ADRESS TELPHONE LOCATION
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_facility",
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_store",
    )


class MobileNetWork(Facility):  # شركات محمول
    code = models.CharField(max_length=5, blank=True, null=True, unique=True)
    emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)


class Compony(Facility):  # شركات
    pass


class ScientificCompany(Compony):  # شركات مستلزمات معامل
    pass


class PharmaceuticalCompany(Compony):  # شركات أدويه
    pass


class Supplier(Compony):
    pass
    # brands = ArrayReferenceField(to=Brand, on_delete=models.CASCADE)


class MedicalFacility(Facility):  # منشأه طبيه
    technical_supervisor = models.ForeignKey(
        to="Persons.Pharmacist", on_delete=models.CASCADE
    )


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


class Shop(Facility):  # محل
    pass


class Butcher(Shop):  # جزاره
    pass


class Grocery(Shop):  # بقاله
    pass


class Barber(Shop):  # محل حلاقه
    pass


class Associations(Facility):  # الجمعيات
    pass


class Department(PolymorphicModel, BaseModelName):
    pass


class NREntity(PolymorphicModel):
    pass


class Laboratory(Facility):
    pass


class MainLab(Laboratory):
    pass


class Lab(Laboratory):
    pass


class LabDepartment(Department):
    pass


class LabJob(Job):
    department = models.ForeignKey(LabDepartment, on_delete=models.CASCADE)
