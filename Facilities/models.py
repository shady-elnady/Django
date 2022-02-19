from django.db import models

# from djongo.models import ArrayReferenceField
# from Persons.models import Person, Pharmacist
from GraphQL.models import BaseModel, BaseModelLogo, BaseModelName
from polymorphic.models import PolymorphicModel
from django.utils.translation import gettext_lazy as _

from Location.models import Caller


# Create your models here.


class Job(PolymorphicModel, BaseModelName):
    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class Facility(PolymorphicModel, BaseModelLogo):  # منشاءت
    owner = models.ForeignKey(
        to="Persons.Person",
        on_delete=models.CASCADE,
        verbose_name=_("Owner"),
    )
    caller = models.ForeignKey(
        Caller,
        on_delete=models.CASCADE,
        verbose_name=_("Caller"),
        related_name="%(app_label)s_%(class)s_Caller",
    )

    class Meta:
        verbose_name = _("Facility")
        verbose_name_plural = _("Facilities")


class Store(Facility):  # مخازن
    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")


class Branch(BaseModelName, BaseModel):
    # TODO ADRESS TELPHONE LOCATION
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_facility",
        verbose_name=_("Facility"),
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_store",
        verbose_name=_("Store"),
    )

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branchs")


class MobileNetWork(Facility):  # شركات محمول
    tel_code = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Tel Code"),
    )
    emoji = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Emoji"),
    )

    class Meta:
        verbose_name = _("Mobile NetWork")
        verbose_name_plural = _("Mobile NetWorks")


class Compony(Facility):  # شركات
    class Meta:
        verbose_name = _("Compony")
        verbose_name_plural = _("Componies")


class ScientificCompany(Compony):  # شركات مستلزمات معامل
    class Meta:
        verbose_name = _("Scientific Company")
        verbose_name_plural = _("Scientific Companies")


class PharmaceuticalCompany(Compony):  # شركات أدويه
    class Meta:
        verbose_name = _("Pharmaceutical Company")
        verbose_name_plural = _("Pharmaceutical Companies")


class Supplier(Compony):
    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    # brands = ArrayReferenceField(to=Brand, on_delete=models.CASCADE)


class MedicalFacility(Facility):  # منشأه طبيه
    technical_supervisor = models.ForeignKey(
        to="Persons.Pharmacist",
        on_delete=models.CASCADE,
        verbose_name=_("Technical Supervisor"),
    )

    class Meta:
        verbose_name = _("Medical Facility")
        verbose_name_plural = _("Medical Facilities")


class Pharmacy(MedicalFacility):  # صيدليات
    class Meta:
        verbose_name = _("Pharmacy")
        verbose_name_plural = _("Pharmacies")


class Clinic(MedicalFacility):  # عيادات
    class Meta:
        verbose_name = _("Clinic")
        verbose_name_plural = _("Clinics")


class DentalClinic(Clinic):  # عيادات اسنان
    class Meta:
        verbose_name = _("Dental Clinic")
        verbose_name_plural = _("Dental Clinics")


class PrivateClinic(Clinic):  # هيادات خاصه
    class Meta:
        verbose_name = _("Private Clinic")
        verbose_name_plural = _("Private Clinics")


class Dispensary(MedicalFacility):  #  المستوصفات
    class Meta:
        verbose_name = _("Dispensary")
        verbose_name_plural = _("Dispensaries")


class Shop(Facility):  # محل
    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")


class Butcher(Shop):  # جزاره
    class Meta:
        verbose_name = _("Butcher")
        verbose_name_plural = _("Butchers")


class Grocery(Shop):  # بقاله
    class Meta:
        verbose_name = _("Grocery")
        verbose_name_plural = _("Groceries")


class Barber(Shop):  # محل حلاقه
    class Meta:
        verbose_name = _("Barber")
        verbose_name_plural = _("Barbers")


class Association(Facility):  # الجمعيات
    class Meta:
        verbose_name = _("Association")
        verbose_name_plural = _("Associations")


class Department(PolymorphicModel, BaseModelName):
    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")


class Laboratory(Facility):
    class Meta:
        verbose_name = _("Laboratory")
        verbose_name_plural = _("Laboratories")


class MainLab(Laboratory):
    class Meta:
        verbose_name = _("Main Laboratory")
        verbose_name_plural = _("Main Laboratories")


class Lab(Laboratory):
    class Meta:
        verbose_name = _("Lab")
        verbose_name_plural = _("Labs")


class LabDepartment(Department):
    class Meta:
        verbose_name = _("Laboratory Department")
        verbose_name_plural = _("Laboratory Departments")


class LabJob(Job):
    department = models.ForeignKey(
        LabDepartment,
        on_delete=models.CASCADE,
        verbose_name=_("Department"),
    )

    class Meta:
        verbose_name = _("Laboratory Job")
        verbose_name_plural = _("Laboratory Jobs")
