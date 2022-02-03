from django.db import models
from djongo.models import ArrayReferenceField
from GraphQL.models import BaseModel, BaseModelName
from Facilities.models import MainLab, NREntity
from Products.models import LineInInvoice, Product, Unit


# Create your models here.


class Stock(BaseModel):  # المخزون
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    details = ArrayReferenceField(
        LineInInvoice,
        on_delete=models.CASCADE,
    )

    @property
    def packing(self):
        return self.product.packing

    @property  # inventory  المخزون
    def stock(self):
        return sum(list(map(lambda x: x["count_packing"], self.details)))


# TODO Duration Sample
class Sample(BaseModelName):
    Comment = models.TextField(max_length=200)
    time = models.TimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)


class TechniqueMethod(BaseModelName):
    pass


class MedicalSupplies(Product):
    pass


class Analyzer(Product):
    brochu_url = models.CharField(max_length=50, null=True, blank=True)
    test_volume = models.DecimalField(max_digits=2, decimal_places=2)


class Kat(Product):
    technique_method = models.ManyToManyField(
        TechniqueMethod,
        through="KatTechniqueMethod",
        symmetrical=False,
    )


class KatTechniqueMethod(models.Model):
    kat = models.ForeignKey(Kat, on_delete=models.CASCADE)
    technique_method = models.ForeignKey(TechniqueMethod, on_delete=models.CASCADE)
    analyzer = models.ManyToManyField(
        Analyzer,
        through="AnalyzerKatTechniqueMethod",
        symmetrical=False,
    )

    class Meta:
        unique_together = [["kat", "technique_method"]]


# NOTE Bind with Medicin
class DisksAntiBiotics(Kat):
    code = models.CharField(max_length=10, unique=True)
    for_child_pregnant = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.code



class ShortCutParameter(BaseModelName):
    pass


class Parameter(BaseModelName):
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


class AnalyzerKatTechniqueMethod(models.Model):
    analyzer = models.ForeignKey(
        Analyzer,
        on_delete=models.CASCADE,
    )
    kat_technique_method = models.ForeignKey(
        KatTechniqueMethod,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = [["analyzer", "kat_technique_method"]]


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

    analyzer_kat_technique_method = models.ManyToManyField(
        AnalyzerKatTechniqueMethod,
        through="Analysis",
    )

    class Meta:
        unique_together = [["parameter", "sample"]]

    def __str__(self) -> str:
        return f"{self.sample}_{self.parameter}"


class Analysis(models.Model):
    shortcuts = ArrayReferenceField(
        to=ShortCutParameter,
        on_delete=models.CASCADE,
    )
    sample_parameter = models.ForeignKey(
        SampleParameter,
        on_delete=models.CASCADE,
    )
    analyzer_kat_technique_method = models.ForeignKey(
        AnalyzerKatTechniqueMethod,
        on_delete=models.CASCADE,
    )
    is_default = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    price_patient = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    price_lab = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    lab_2_lab = models.ManyToManyField(
        MainLab,
        through="MainLabMenu",
    )
    # TODO Normal Range
    normal_range = models.ManyToManyField(
        NREntity,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = [
            [
                "sample_parameter",
                "analyzer_kat_technique_method",
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
    cost = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )  # التكلفه
    # TODO RUN TIME handle Duration is best from TextChoices
    run_time = models.CharField(max_length=20, choices=RunTime.choices)
    # TODO Normal Range
    normal_range = models.ManyToManyField(
        NREntity,
        null=True,
        blank=True,
    )
    is_default = models.BooleanField(default=True)

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

    name = models.CharField(max_length=5, primary_key=True, choices=HL.choices)


class Departement(BaseModelName):
    pass


# class Telephone(BaseModelNative):
#     pass


#  🧕   🕌   🕋  👳  💲  🌍  👰‍♂️   👰‍♀️   👩‍❤️‍💋‍👩   🤰🏻   🏋️‍♀️   💒   👩‍❤️‍💋‍👨   🧑🏼‍🍼  👩‍🎓   🚣‍♀️  🤾‍♀️  👨‍💼   👷🏽‍♂️  👷🏼‍♀️   👨‍🔧   👨‍⚕  👩🏽‍⚕️  👨🏻‍🎓  👨🏼‍🏫  👩🏽‍🏫   🦷
