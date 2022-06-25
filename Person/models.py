# from unicodedata import category as _category
from django.db import models  # from django.db.models import Model, ForeignKey, CASCADE
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from PIL import Image
from datetime import date
import calendar

from .managers import FollowingManager, UsersManager
from GraphQL.models import BaseModel, BaseModelName, BaseModelNative, Shifts, WeekDays
from Facility.models import Branch, Job
from polymorphic.models import PolymorphicModel
from djongo.models import ArrayReferenceField
from Language.models import Language
from Location.models import Contacts


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
    contact_method = models.ForeignKey(
        Contacts,
        on_delete=models.CASCADE,
        verbose_name=_("Contact_Method"),
        related_name="%(app_label)s_%(class)s_Contact_Method",
    )  # طرق الاتصال

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


class kinshipRelations(models.TextChoices):
    Father = _("Father")
    Mother = _("Mother")
    Brother = _("Brother")
    Sister = _("Sister")


class Kinship(models.Model):

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
    )
    kinshiper = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name=_("Kinshiper"),
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


class Patient(Person):
    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")


# TODO Permission class Bind to MIXIN
class Permission(BaseModelName, PermissionsMixin):
    class Meta:
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")


class Employee(Person):

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name=_("Branch"),
        related_name="%(app_label)s_%(class)s_Branch",
    )
    salary = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Salary"),
    )
    is_former_employee = models.BooleanField(
        default=False,
        verbose_name=_("is Former Employee"),
    )  # موظف سابق

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")


class User(Person, AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=False,
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("Permissions"),
        related_name="%(app_label)s_%(class)s_Permissions",
    )
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Last LogIn"),
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    objects = UsersManager()

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
        default="images/Profiles/default_profile.jpg",
        upload_to="images/Profiles/",
        blank=True,
        null=True,
    )
    skills = models.CharField(max_length=100, null=True, blank=True)

    @property
    def slug(self):
        return slugify(str(self.user))

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self):
        super().save()

        img = Image.open(self.profile_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class MedicalSpecialization(BaseModelName):
    class Meta:
        verbose_name = _("Specialization")
        verbose_name_plural = _("Specializations")


class Doctor(Person):
    medical_specialization = models.ForeignKey(
        MedicalSpecialization,
        on_delete=models.CASCADE,
        verbose_name=_("Medical Specialization"),
        related_name="%(app_label)s_%(class)s_Medical_Specialization",
    )

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
