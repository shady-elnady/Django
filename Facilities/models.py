from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from polymorphic.models import PolymorphicModel
from GraphQL.models import (
    BaseModel,
    BaseModelLogo,
    BaseModelName,
    FacilityTypes,
    Shifts,
    WeekDays,
)
from Location.models import Contacts

# Create your models here.


class Shift(PolymorphicModel, BaseModel):  # شفتات ايام الاسبوع

    week_day = models.CharField(
        max_length=10,
        choices=WeekDays.choices,
        verbose_name=_("Week Day"),
        related_name="%(app_label)s_%(class)s_Week_Day",
    )
    shift = models.CharField(
        max_length=10,
        choices=Shifts.choices,
        verbose_name=_("Shift"),
        related_name="%(app_label)s_%(class)s_Shift",
    )
    attending_time = models.TimeField(verbose_name=_("Attending Time"))  # الحضور
    leaving_time = models.TimeField(verbose_name=_("Leaving Time"))  # الانصراف

    @property
    def name(self):
        return f"{self.week_day} - {self.shift}"

    @property
    def slug(self):
        return slugify(f"{self.week_day} - {self.shift}")

    def __str__(self):
        return f"{self.week_day} - {self.shift}"

    @property
    def shift_hours(self):
        return self.leaving_time - self.attending_time

    class Meta:
        unique_together = [["week_day", "shift"]]
        verbose_name = _("Shift")
        verbose_name_plural = _("Shifts")


class Job(BaseModelName):
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
    facility_type = models.CharField(
        max_length=35,
        choice=FacilityTypes.choices,
        verbose_name=_("Facility Type"),
        related_name="%(app_label)s_%(class)s_Facility_Type",
    )

    class Meta:
        verbose_name = _("Facility")
        verbose_name_plural = _("Facilities")


class Store(BaseModelName):  # مخازن

    owner_facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_Owner_Facility",
        verbose_name=_("Owner Facility"),
    )

    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")


class Branch(BaseModelName, BaseModel):

    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_Facility",
        verbose_name=_("Facility"),
    )
    contact_method = models.ForeignKey(
        Contacts,
        on_delete=models.CASCADE,
        verbose_name=_("Contact_Method"),
        related_name="%(app_label)s_%(class)s_Contact_Method",
    )  # طرق الاتصال

    class Meta:
        verbose_name = _("Branch")
        verbose_name_plural = _("Branchs")


class MobileNetWork(Facility):  # شركات محمول

    telephone_code = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Telephone Code"),
    )

    class Meta:
        verbose_name = _("Mobile NetWork")
        verbose_name_plural = _("Mobile NetWorks")


"""

class MedicalFacility(Facility):  # منشأه طبيه
    technical_supervisor = models.ForeignKey(
        to="Persons.Person",
        on_delete=models.CASCADE,
        verbose_name=_("Technical Supervisor"),
    )

    class Meta:
        verbose_name = _("Medical Facility")
        verbose_name_plural = _("Medical Facilities")


class Laboratory(Facility):
    class Meta:
        verbose_name = _("Laboratory")
        verbose_name_plural = _("Laboratories")


class Compony(Facility):  # شركات
    class Meta:
        verbose_name = _("Compony")
        verbose_name_plural = _("Componies")


class Shop(Facility):  # المحلات
    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")


class Association(Facility):  # الجمعيات
    class Meta:
        verbose_name = _("Association")
        verbose_name_plural = _("Associations")


class Dispensary(MedicalFacility):  #  المستوصفات
    class Meta:
        verbose_name = _("Dispensary")
        verbose_name_plural = _("Dispensaries")




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




class Department(PolymorphicModel, BaseModelName):
    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")




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
"""
