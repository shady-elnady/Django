# from unicodedata import category as _category
from django.db import models  # from django.db.models import Model, ForeignKey, CASCADE
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from datetime import date
import calendar

from .managers import FollowingManager, UsersManager
from GraphQL.models import BaseModel, BaseModelName
from Facilities.models import Branch, Job
from polymorphic.models import PolymorphicModel
from djongo.models import ArrayReferenceField
from Languages.models import Language
from Location.models import Caller


# Create your models here.


class ReferenceLimitingFactor(PolymorphicModel, BaseModelName):
    category = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name=_("Category"),
        related_name="%(app_label)s_%(class)s_Category",
    )

    class Meta:
        verbose_name = _("Reference Limiting Factor")
        verbose_name_plural = _("Reference Limiting Factors")


class MaritalStatus(BaseModelName):
    emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Marital Status")
        verbose_name_plural = _("Marital Status")


class Gender(ReferenceLimitingFactor):
    emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Gender")
        verbose_name_plural = _("Genders")


class Person(PolymorphicModel, BaseModel):

    national_id = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("National ID"),
    )
    full_name = models.CharField(
        max_length=80,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Full Name"),
    )
    family_name = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("Family Name"),
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Birth Date"),
    )
    gender = models.ForeignKey(
        Gender,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Gender"),
    )
    marital_status = models.ForeignKey(
        MaritalStatus,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Marital Status"),
    )  # الحاله الاجتماعيه
    Job = models.ForeignKey(
        Job,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Job"),
    )
    kinshipers = models.ManyToManyField(
        "self",
        through="Kinship",
        symmetrical=True,
        verbose_name=_("Kinshipers"),
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default="ar",
        verbose_name=_("Language"),
    )
    caller = models.ForeignKey(
        Caller,
        on_delete=models.CASCADE,
        verbose_name=_("Caller"),
        related_name="%(app_label)s_%(class)s_Caller",
    )

    @property
    def age(self):
        born = self.birth_date
        calendar.setfirstweekday(calendar.SUNDAY)
        today = date.today()
        if today.month >= born.month:
            year = today.year
        else:
            year = today.year - 1
        age_years = year - born.year
        try:  # raised when birth day is February 29 and the current year is not a leap year
            age_days = (today - (born.replace(year=year))).days
        except ValueError:
            age_days = (today - (born.replace(year=year, day=born.day - 1))).days + 1
        month = born.month
        age_months = 0
        while age_days > calendar.monthrange(year, month)[1]:
            age_days = age_days - calendar.monthrange(year, month)[1]
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
            age_months += 1
        return f"{age_years} {age_months} {age_days}"

    @property
    def slug(self):
        return slugify(str(self.full_name))

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")


class Kinship(models.Model):
    class kinshipRelations(models.TextChoices):
        a = "a"

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )
    kinshiper = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_kinshiper",
    )
    Relation = models.CharField(
        max_length=20,
        choices=kinshipRelations.choices,
    )

    @property
    def slug(self):
        return slugify(str(self.person))

    def __str__(self):
        return f"{self.person} -> {self.kinshiper}"

    class Meta:
        unique_together = (
            "person",
            "kinshiper",
        )
        verbose_name = _("Kinship")
        verbose_name_plural = _("Kinships")


# class Pharmacist(Person):  # صيدلي
#     class Meta:
#         verbose_name = _("Pharmacist")
#         verbose_name_plural = _("Pharmacists")


# class Customer(Person):
#     class Meta:
#         verbose_name = _("Customer")
#         verbose_name_plural = _("Customers")


class Patient(Person):
    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")


# TODO Permission class Bind to MIXIN
class Permission(BaseModelName):
    class Meta:
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")


class Employee(Person):

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=5, decimal_places=2)
    attendance_time = models.TimeField()  # ميعاد الحضور
    check_out_time = models.TimeField()  # ميعاد الانصراف
    permissions = ArrayReferenceField(
        to=Permission,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")


class User(Person, AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UsersManager()

    username = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=False,
    )
    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Following(BaseModel):
    followed = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_follower",
    )

    class Meta:
        unique_together = (
            "followed",
            "follower",
        )
        verbose_name = _("Following")
        verbose_name_plural = _("Followings")

    objects = FollowingManager()

    @property
    def slug(self):
        return slugify(str(self.followed))

    def __str__(self):
        return self.followed


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        default="images/default_profile_img.jpg",
        upload_to="user_profile_img",
        blank=True,
        null=True,
    )
    skills = models.CharField(max_length=100, null=True, blank=True)

    @property
    def slug(self):
        return slugify(str(self.user))

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class Specialization(BaseModelName):
    class Meta:
        verbose_name = _("Specialization")
        verbose_name_plural = _("Specializations")


class Doctor(Person):
    specialization = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")


class LabEmployee(Employee):
    class Meta:
        verbose_name = _("Lab Employee")
        verbose_name_plural = _("Lab Employees")


# TODO Employee Attendance Management System
## https://itsourcecode.com/uml/employee-attendance-management-system-er-diagram-erd/


class Work(BaseModelName):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")


class Duty(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    duration = models.DurationField()
    _date = models.DateField()

    class Meta:
        verbose_name = _("Duty")
        verbose_name_plural = _("Duties")


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    _date = models.DateField()

    class Meta:
        verbose_name = _("Leave")
        verbose_name_plural = _("Leaves")


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    duty = models.ForeignKey(Duty, on_delete=models.CASCADE)
    total_labor = models.DecimalField(max_digits=5, decimal_places=2)
    salary = models.DecimalField(max_digits=5, decimal_places=2)
    _date = models.DateField()

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")
