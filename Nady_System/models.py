from django.db import models
from Facilities.models import Facility, MainLab, Store
from GraphQL.models import BaseModel, BaseModelName, BaseModelNative
from djongo.models import ArrayReferenceField
from Persons.models import Employee
from Products.models import Product

# Create your models here.

# TODO
class LabWork(BaseModelName):
    pass
    # Admin = 'Admin'
    # Reciption = 'Reciption'
    # Nurse = 'Nurse'
    # Spicialiste = 'Spicialiste'
    # Representative = 'Representative'


class LabEmployee(Employee):
    works = ArrayReferenceField(
        to=LabWork,
        on_delete=models.CASCADE,
    )


# TODO
class Laboratory(Facility):
    pass


class MainLab(Laboratory):
    pass


class Lab(Laboratory):
    pass


# TODO
class ItemDetail(BaseModel):
    quantity = models.DecimalField(max_digits=3, decimal_places=2)
    expire_date = models.DateField()


class Stock(BaseModel):  # المخزون
    item = models.OneToOneField(Product, on_delete=models.CASCADE)
    details = models.ManyToManyField(
        ItemDetail,
        on_delete=models.CASCADE,
    )


# TODO
class Sample(BaseModelName):
    Comment = models.TextField(max_length=200)


class TechniqueMethod(BaseModelName):
    pass


class Kat(Product):
    pass


class MedicalSupplies(Product):
    pass


class Analyzer(Product):
    brochu_url = models.CharField(max_length=50, null=True, blank=True)
    test_volume = models.DecimalField(max_digits=2, decimal_places=2)


# NOTE Bind with Medicin
class DisksAntiBiotics(Kat):
    code = models.CharField(max_length=10, unique=True)
    for_child_pregnant = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.code


class Unit(BaseModelName):
    units_related = models.ManyToManyField(
        "self",
        through="UnitConvert",
        symmetrical=False,
    )


class UnitConvert(models.Model):
    from_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
    )
    to_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
    )
    factor = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        unique_together = [["from_unit", "to_unit"]]


class ShortCutParameter(BaseModelName):
    pass


class Parameter(BaseModelName):
    shortcuts = ArrayReferenceField(
        to=ShortCutParameter,
        on_delete=models.CASCADE,
    )
    samples = models.ManyToManyField(
        Sample,
        through="SampleParameter",
        symmetrical=False,
    )
    units = models.ManyToManyField(
        Unit,
        through="ParameterUnit",
        symmetrical=False,
    )


class ParameterUnit(models.Model):
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
    )
    is_default = models.BooleanField(default=True)
    parameter_unit_related = models.ManyToManyField(
        "self",
        through="ParameterUnitConvert",
        symmetrical=False,
    )

    def __str__(self) -> str:
        return f"{self.parameter}_{self.unit}"

    class Meta:
        unique_together = [["parameter", "unit"]]


class ParameterUnitConvert(models.Model):
    from_parameter_unit = models.ForeignKey(
        ParameterUnit,
        on_delete=models.CASCADE,
    )
    to_parameter_unit = models.ForeignKey(
        ParameterUnit,
        on_delete=models.CASCADE,
    )
    factor = models.DecimalField(max_digits=5, decimal_places=4)

    class Meta:
        unique_together = [["from_parameter_unit", "to_parameter_unit"]]

    def __str__(self) -> str:
        return f"{self.from_parameter_unit} -> {self.to_parameter_unit}"


class SampleParameter(models.Model):
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
    )
    sample = models.ForeignKey(
        Sample,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # analyzer = models.ManyToManyField(
    #     Analyzer,
    #     through="Analysis",
    #     symmetrical=False,
    # )
    # kat = models.ManyToManyField(
    #     Kat,
    #     through="kat",
    #     symmetrical=False,
    # )
    # technique_method = models.ManyToManyField(
    #     TechniqueMethod,
    #     through="Analysis",
    #     symmetrical=False,
    # )

    # NOTE
    # is_default = models.BooleanField(default=True)
    # is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = [["parameter", "sample"]]

    def __str__(self) -> str:
        return f"{self.sample}_{self.parameter}"


class Analysis(BaseModelName):
    sample_parameter = models.ForeignKey(
        SampleParameter,
        on_delete=models.CASCADE,
    )
    analyzer = models.ForeignKey(
        Analyzer,
        on_delete=models.CASCADE,
    )
    technique_method = models.ForeignKey(
        TechniqueMethod,
        on_delete=models.CASCADE,
    )
    kat = models.ForeignKey(
        Kat,
        on_delete=models.CASCADE,
    )
    price_ptient = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    price_lab_2_we = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    my_lab_2_lab = models.ManyToManyField(
        MainLab,
        through="MainLabMenu",
    )
    normal_range = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = [
            [
                "sample_parameter",
                "analyzer",
                "technique_method",
                "kat",
            ]
        ]


class MainLabMenu(models.Model):
    class RunTime(models.TextChoices):
        SameDay = "Same Day"
        NextDay = "Next Day"
        TwoDays = "Two Day3"
        NextWeak = "Next Weak"
        Monday = "Monday"
        Tuesday = "Tuesday"
        Wednesday = "Wednesday"
        Thursday = "Thursday"
        Friday = "Friday"
        Saturday = "Saturday"
        Sunday = "Sunday"

    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    laboratory = models.ForeignKey(MainLab, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    run_time = models.CharField(max_length=20, choices=RunTime.choices)
    normal_range = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    default = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            [
                "analysis",
                "laboratory",
            ]
        ]


class BloodGroup(BaseModelName):  # ENUM
    class ABOSystem(models.TextChoices):
        A = "A"
        B = "B"
        AB = "AB"
        O = "O"

    class Rh_Type(models.TextChoices):
        Positive = "Positive"
        Negative = "Negative"

    ABO_system = models.CharField(max_length=2, choices=ABOSystem.choices)
    Rh_type = models.CharField(max_length=10, choices=Rh_Type.choices)

    class Meta:
        unique_together = (
            "ABO_system",
            "Rh_type",
        )


class Senstivity(models.Model):  # ENUM
    class Senstive(models.TextChoices):
        Strong = "Strong"
        Mmderate = "Moderate"
        weak = "Weak"
        very_weak = "Very Weak"

    name = models.CharField(max_length=10, primary_key=True, choices=Senstive.choices)


class HighLow(models.Model):  # ENUM
    class HL(models.TextChoices):
        high = "High"
        low = "Low"

    name = models.CharField(max_length=10, primary_key=True, choices=HL.choices)


class Departement(BaseModelName):
    pass


# class Telephone(BaseModelNative):
#     pass


#  🧕   🕌   🕋  👳  💲  🌍  👰‍♂️   👰‍♀️   👩‍❤️‍💋‍👩   🤰🏻   🏋️‍♀️   💒   👩‍❤️‍💋‍👨   🧑🏼‍🍼  👩‍🎓   🚣‍♀️  🤾‍♀️  👨‍💼   👷🏽‍♂️  👷🏼‍♀️   👨‍🔧   👨‍⚕  👩🏽‍⚕️  👨🏻‍🎓  👨🏼‍🏫  👩🏽‍🏫   🦷
