# from Facilities.models import Branch, Department
from Languages.models import Language
from Nady_System.models import NREntity
from Persons.managers import FollowingManager, UsersManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models  # from django.db.models import Model, ForeignKey, CASCADE

from djongo.models import ArrayReferenceField
from GraphQL.models import BaseModel, BaseModelName

# from Nady_System.models import BloodGroup
from polymorphic.models import PolymorphicModel
import calendar
from datetime import date

# from django.apps import apps
# MyModel = apps.get_model('myapp', 'MyModel')


# Create your models here.


class StageLife(NREntity, BaseModelName):
    from_age = models.DurationField()
    to_age = models.DurationField()


class MaritalStatus(BaseModelName):
    emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=False)


class Job(PolymorphicModel, BaseModelName):
    pass


###################################
class Gender(NREntity, BaseModelName):
    emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)
    is_active = models.BooleanField(default=False)


class Title(BaseModelName):
    stage_life = models.ForeignKey(
        StageLife,
        on_delete=models.CASCADE,
    )
    gender = models.ForeignKey(
        Gender,
        on_delete=models.CASCADE,
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = (
            "stage_life",
            "job",
            "gender",
        )


class Person(PolymorphicModel, BaseModel):

    national_id = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True,
    )
    full_name = models.CharField(max_length=80, unique=True)
    family_name = models.CharField(max_length=15)
    birth_date = models.DateField()
    image_url = models.ImageField(
        upload_to="images",
        editable=True,
        null=True,
        blank=True,
    )
    gender = models.ForeignKey(
        Gender,
        on_delete=models.CASCADE,
    )
    marital_status = models.ForeignKey(
        MaritalStatus,
        on_delete=models.CASCADE,
    )  # الحاله الاجتماعيه
    Job = models.ForeignKey(
        Job,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    kinshipers = models.ManyToManyField(
        "self",
        through="Kinship",
        symmetrical=True,
    )
    email = models.EmailField(
        max_length=200,
        unique=True,
        null=False,
        blank=False,
    )  # TODO E-mail

    @property
    def title(self) -> str:
        return Title.objects.get(name=self.job).name

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

    def __str__(self) -> str:
        return self.full_name


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
    )
    Relation = models.CharField(
        max_length=20,
        choices=kinshipRelations.choices,
    )

    class Meta:
        unique_together = (
            "person",
            "kinshiper",
        )


# class Pharmaceutical(Product):
#     pass


class Pharmacist(Person):  # صيدلي
    pass


class Customer(Person):
    pass


class Patient(Person):
    pass
    # blood_group = models.ForeignKey(
    #     BloodGroup, on_delete=models.CASCADE, blank=True, null=True,
    # )


# TODO Permission class Bind to MIXIN
class Permission(BaseModelName):
    pass


class Employee(Person):
    branch = models.ForeignKey(to="Facilities.Branch", on_delete=models.CASCAD)
    salary = models.DecimalField(max_digits=5, decimal_places=2)
    attendance_time = models.TimeField()  # ميعاد الحضور
    check_out_time = models.TimeField()  # ميعاد الانصراف
    permissions = ArrayReferenceField(
        to=Permission,
        on_delete=models.CASCADE,
    )


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
    language = models.ForeignKey(
        Language, on_delete=models.SET_NULL, null=True, blank=True
    )
    is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)


class Following(BaseModel):
    followed = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "followed",
            "follower",
        )

    objects = FollowingManager()


# TODO Employee Attendance Management System
## https://itsourcecode.com/uml/employee-attendance-management-system-er-diagram-erd/


class Work(BaseModelName):
    department = models.ForeignKey(to="Facilities.Department", on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)


class Duty(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    duration = models.DurationField()
    _date = models.DateField()


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    _date = models.DateField()


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    duty = models.ForeignKey(Duty, on_delete=models.CASCADE)
    total_labor = models.DecimalField(max_digits=5, decimal_places=2)
    salary = models.DecimalField(max_digits=5, decimal_places=2)
    _date = models.DateField()
