from django.db import models
from djongo.models import ArrayReferenceField
from polymorphic.models import PolymorphicModel
from GraphQL.models import BaseModel, BaseModelName
from Facilities.models import Branch, Job, MainLab
from Persons.models import Doctor, Gender, LabEmployee, ReferenceLimitingFactor, Patient
from Products.models import Brand, LineInInvoice, MedicalSupply, Unit
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from GraphQL.custom_fields import QRField


# Create your models here.


class StageLife(ReferenceLimitingFactor):
    start_from_age = models.DurationField(verbose_name=_("Start from Age"))
    end_to_age = models.DurationField(verbose_name=_("End to Age"))

    class Meta:
        verbose_name = _("Stage Life")
        verbose_name_plural = _("Stage Lifes")

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


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

    @property
    def slug(self):
        return slugify(self.name)

    class Meta:
        unique_together = (
            "stage_life",
            "job",
            "gender",
        )
        verbose_name = _("Title")
        verbose_name_plural = _("Titles")


class AnalyticalTechnique(BaseModelName):
    class Meta:
        verbose_name = _("Technique Method")
        verbose_name_plural = _("Technique Methods")


class LabSupply(MedicalSupply):
    class Meta:
        verbose_name = _("Laboratory Supply")
        verbose_name_plural = _("Laboratories Supplies")


class Analyzer(LabSupply):
    class Analyzers(models.TextChoices):
        HematolgyAnalyzer = "HematolgyAnalyzer"
        ElectrolyteAnalyzer = "ElectrolyteAnalyzer"
        UrineAnalyzer = "UrineAnalyzer"
        ChemistryAnalyzer = "ChemistryAnalyzer"

    type = models.CharField(
        max_length=20,
        verbose_name=_("Type"),
        choices=Analyzers.choices,
    )
    brochu_url = models.FileField(
        upload_to="Brochu/Analyzers/",
        verbose_name=_("Brouchu URL"),
        null=True,
        blank=True,
    )
    test_volume = models.DecimalField(
        max_digits=2,
        decimal_places=2,
        verbose_name=_("Test Volume"),
    )
    analytical_technique = models.ManyToManyField(
        AnalyticalTechnique,
        verbose_name=_("Analytical Technique"),
        related_name="%(app_label)s_%(class)s_Analytical_Technique",
    )

    class Meta:
        verbose_name = _("Analyzer")
        verbose_name_plural = _("Analyzers")


class ClosedSystemAnalyzer(Analyzer):
    class Meta:
        verbose_name = _("Closed System Analyzer")
        verbose_name_plural = _("Closed System Analyzers")


class Container(LabSupply):
    class Meta:
        verbose_name = _("Container")
        verbose_name_plural = _("Containers")


class Specimen(BaseModelName):
    class TypeSpecimen(models.TextChoices):
        BodyLiquid = ""
        Tissue = ""
        SolidSpecimen = ""
        GasSpecimen = ""
        Swab = ""

    containers = models.ManyToManyField(
        Container,
        through="Sample",
        verbose_name=_("Containers"),
        related_name="%(app_label)s_%(class)s_Containers",
    )
    reference_limiting_factor = models.ManyToManyField(
        ReferenceLimitingFactor,
        through="Sample",
        verbose_name=_("Reference Limiting Factor"),
        related_name="%(app_label)s_%(class)s_Reference_Limiting_Factor",
    )
    type = models.CharField(
        max_length=20,
        verbose_name=_("Type"),
        choices=TypeSpecimen.choices,
    )

    class Meta:
        verbose_name = _("Specimen")
        verbose_name_plural = _("Specimens")


# TODO Duration Sample
class Sample(BaseModelName):
    # class Action(models.TextChoices):
    #     Prandial = "Prandial"

    specimen = models.ForeignKey(
        Specimen,
        on_delete=models.CASCADE,
        verbose_name=_("Specimen"),
        related_name="%(app_label)s_%(class)s_Specimen",
    )
    container = models.ForeignKey(
        Container,
        on_delete=models.CASCADE,
        verbose_name=_("Container"),
        related_name="%(app_label)s_%(class)s_Container",
    )
    reference_limiting_factor = models.ForeignKey(
        ReferenceLimitingFactor,
        on_delete=models.CASCADE,
        verbose_name=_("Reference Limiting Factor"),
        related_name="%(app_label)s_%(class)s_Reference_Limiting_Factor",
    )
    comments = models.TextField(
        max_length=200,
        verbose_name=_("Comments"),
    )
    # TODO ADD in ReferenceLimitingFactor
    # time = models.TimeField(
    #     blank=True,
    #     null=True,
    #     verbose_name=_("Time"),
    # )
    # action_binding = models.CharField(
    #     max_length=20,
    #     verbose_name=_("Action Binding"),
    #     choices=Action.choices,
    #     blank=True,
    #     null=True,
    # )
    # duration_action = models.DurationField(
    #     blank=True,
    #     null=True,
    #     verbose_name=_("Duration Action"),
    # )

    class Meta:
        unique_together = [["specimen", "container", "reference_limiting_factor"]]
        verbose_name = _("Sample")
        verbose_name_plural = _("Samples")


class Analysis(BaseModelName, PolymorphicModel):

    lab2lab = models.ManyToManyField(
        MainLab,
        verbose_name=_("Lab 2 Lab"),
        through="MainLabMenu",
        related_name="%(app_label)s_%(class)s_Lab_2_Lab",
    )
    price_patient = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=_("Price Patient"),
    )
    price_labs = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=_("Price Labs"),
    )

    class Meta:
        verbose_name = _("Analysis")
        verbose_name_plural = _("Analysis")


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

    analysis = models.ForeignKey(
        Analysis,
        on_delete=models.CASCADE,
        verbose_name=_("Analysis"),
        related_name="%(app_label)s_%(class)s_Analysis",
    )
    laboratory = models.ForeignKey(
        MainLab,
        on_delete=models.CASCADE,
        verbose_name=_("Laboratory"),
        related_name="%(app_label)s_%(class)s_Laboratory",
    )
    cost = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Cost"),
    )  # التكلفه
    # TODO RUN TIME handle Duration is best from TextChoices
    run_time = models.CharField(
        max_length=20,
        choices=RunTime.choices,
        verbose_name=_("Run Time"),
    )
    # TODO Normal Range
    normal_range = models.ForeignKey(
        ENeedNormal,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_Normal_Range",
        verbose_name=_("Normal Range"),
        blank=True,
        null=True,
    )
    is_favorite = models.BooleanField(
        default=True,
        verbose_name=_("is Favorite"),
    )

    def __str__(self):
        return f"{str(self.analysis)}->{str(self.laboratory)}"

    @property
    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [
            [
                "analysis",
                "laboratory",
            ]
        ]
        verbose_name = _("Main Lab Menu")
        verbose_name_plural = _("Main Lab Menus")


class ShortCut(BaseModelName):
    analysis = models.ForeignKey(
        Analysis,
        on_delete=models.CASCADE,
        verbose_name=_("Analysis"),
        related_name="%(app_label)s_%(class)s_Analysis",
    )

    class Meta:
        verbose_name = _("ShortCut")
        verbose_name_plural = _("ShortCuts")


class Package(Analysis):
    contain = models.ManyToManyField(
        Analysis,
        verbose_name=_("Contain"),
        related_name="%(app_label)s_%(class)s_Contain",
    )

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")


class Report(Analysis):
    contain = models.ManyToManyField(
        Analysis,
        verbose_name=_("Contain"),
        related_name="%(app_label)s_%(class)s_Contain",
    )

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")


class SectionInReport(Analysis):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        verbose_name=_("Report"),
        related_name="%(app_label)s_%(class)s_Report",
    )
    contain = models.ManyToManyField(
        Analysis,
        verbose_name=_("Contain"),
        related_name="%(app_label)s_%(class)s_Contain",
    )

    class Meta:
        verbose_name = _("Section In Report")
        verbose_name_plural = _("Section In Reports")


class SpecialInfo(Analysis):
    class Meta:
        verbose_name = _("Special Info")
        verbose_name_plural = _("Special Infos")


class Parameter(BaseModelName):

    units = models.ManyToManyField(
        Unit,
        verbose_name=_("Units"),
        through="ParameterUnit",
        related_name="%(app_label)s_%(class)s_Units",
    )
    specimens = models.ManyToManyField(
        Specimen,
        verbose_name=_("Specimens"),
        through="SpecimenParameter",
        related_name="%(app_label)s_%(class)s_Specimens",
    )
    # TODO CHEMICAL STRCTURE

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameters")


class ParameterUnit(models.Model):
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        verbose_name=_("Parameter"),
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name=_("Unit"),
    )
    is_favorite = models.BooleanField(
        default=True,
        verbose_name=_("Is Favorite"),
    )

    def __str__(self):
        return f"{self.parameter}->{self.unit}"

    @property
    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [["parameter", "unit"]]
        verbose_name = _("Parameter Unit")
        verbose_name_plural = _("Parameter Units")


class Equation(models.Model):
    equatin = models.CharField(max_length=20)
    parameters = models.ManyToManyField(
        Analysis,
        verbose_name=_("Parameter"),
        # through="ParametersEquation",
        related_name="%(app_label)s_%(class)s_Parameter",
    )

    def __str__(self):
        return f"{self.equatin}->{self.parameter}"

    def slug(self):
        return slugify(self.__str__)

    class Meta:
        verbose_name = _("Equation")
        verbose_name_plural = _("Equations")


class SpecimenParameter(models.Model):
    specimen = models.ForeignKey(
        Specimen,
        on_delete=models.CASCADE,
        verbose_name=_("Specimen"),
        related_name="%(app_label)s_%(class)s_Specimen",
    )
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        verbose_name=_("Parameter"),
        related_name="%(app_label)s_%(class)s_Parameter",
    )
    analysis_technique = models.ManyToManyField(
        AnalyticalTechnique,
        verbose_name=_("Analysis Technique"),
        through="SpecimenParameterTechnique",
        related_name="%(app_label)s_%(class)s_Analysis_Technique",
    )
    reference_limiting_factor = models.ManyToManyField(
        ReferenceLimitingFactor,
        verbose_name=_("Normal Limiting Factor"),
        through="SpecimenParameterNormalLimitingFactor",  ##
        related_name="%(app_label)s_%(class)s_Normal_Limiting_Factor",
    )

    def __str__(self):
        return f"{self.specimen}->{self.parameter}"

    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [["specimen", "parameter"]]
        verbose_name = _("Specimen Parameter")
        verbose_name_plural = _("Specimen Parameters")


class Kat(LabSupply):
    specimen_parameter_technique = models.ManyToManyField(
        to="SpecimenParameterTechnique",
        through="SpecimenParameterTechniqueKat",
        verbose_name=_("Specimen Parameter Technique"),
        related_name="%(app_label)s_%(class)s_Specimen_Parameter_Technique",
    )
    samples = models.ManyToManyField(
        Sample,
        through="KatSample",
        verbose_name=_("Samples"),
        related_name="%(app_label)s_%(class)s_Samples",
    )
    brochu_url = models.FileField(
        upload_to="Brochu/Kats/",
        verbose_name=_("Brouchu URL"),
        null=True,
        blank=True,
    )
    analytical_technique = models.ForeignKey(
        AnalyticalTechnique,
        on_delete=models.CASCADE,
        verbose_name=_("Analytical Technique"),
        related_name="%(app_label)s_%(class)s_Analytical_Technique",
    )

    class Meta:
        verbose_name = _("Kat")
        verbose_name_plural = _("Kats")


class SpecimenParameterTechnique(Analysis):
    specimen_parameter = models.ForeignKey(
        SpecimenParameter,
        on_delete=models.CASCADE,
        verbose_name=_("Specimen Parameter"),
        related_name="%(app_label)s_%(class)s_Specimen_Parameter",
    )
    analytical_technique = models.ForeignKey(
        AnalyticalTechnique,
        on_delete=models.CASCADE,
        verbose_name=_("Analytical Technique"),
        related_name="%(app_label)s_%(class)s_Analytical_Technique",
    )
    calculated_equation = models.ManyToManyField(
        Equation,
        verbose_name=_("Calculated_From"),
        related_name="%(app_label)s_%(class)s_Calculated_Equation",
    )
    kats = models.ManyToManyField(
        Kat,
        through="SpecimenParameterTechniqueKat",
        verbose_name=_("Calculated_From"),
        related_name="%(app_label)s_%(class)s_Calculated_Equation",
    )
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        verbose_name=_("Report"),
        related_name="%(app_label)s_%(class)s_Report",
        blank=True,
        null=True,
    )
    section_in_report = models.ForeignKey(
        SectionInReport,
        on_delete=models.CASCADE,
        verbose_name=_("SectionInReport"),
        related_name="%(app_label)s_%(class)s_SectionInReport",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.specimen_parameter}->{self.analytical_technique}"

    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [["specimen_parameter", "analytical_method"]]
        verbose_name = _("Specimen Parameter Technique")
        verbose_name_plural = _("Specimen Parameter Techniques")


class KatSample(models.Model):
    kat = models.ForeignKey(
        Kat,
        on_delete=models.CASCADE,
        verbose_name=_("Kat"),
        related_name="%(app_label)s_%(class)s_Kat",
    )
    sample = models.ForeignKey(
        Sample,
        on_delete=models.CASCADE,
        verbose_name=_("Sample"),
        related_name="%(app_label)s_%(class)s_Sample",
    )
    is_favorite = models.BooleanField(
        default=True,
        verbose_name=_("Is favorite"),
    )

    def __str__(self):
        return f"{str(self.kat)}->{str(self.sample)}"

    @property
    def slug(self):
        return self.__str__

    class Meta:
        unique_together = [["kat", "sample"]]
        verbose_name = _("Kat Sample")
        verbose_name_plural = _("Kat Samples")


class KatSenstivity(models.Model):
    low = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        verbose_name=_("Low"),
    )
    high = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        verbose_name=_("High"),
    )

    class Meta:
        verbose_name = _("Kat Senstivity")
        verbose_name_plural = _("Kat Senstivities")


class SpecimenParameterTechniqueKat(models.Model):
    kat = models.ForeignKey(
        Kat,
        on_delete=models.CASCADE,
        verbose_name=_("Kat"),
        related_name="%(app_label)s_%(class)s_Kat",
    )
    specimen_parameter_technique = models.ForeignKey(
        SpecimenParameterTechnique,
        on_delete=models.CASCADE,
        verbose_name=_("Specimen Parameter Technique"),
        related_name="%(app_label)s_%(class)s_Specimen_Parameter_Technique",
    )
    normal_range = models.ForeignKey(
        ENeedNormal,
        on_delete=models.CASCADE,
        verbose_name=_("Normal Range"),
        related_name="%(app_label)s_%(class)s_Normal_Range",
    )
    kat_sensitivity = models.ForeignKey(
        KatSenstivity,
        on_delete=models.CASCADE,
        verbose_name=_("Kat Senstivity"),
        related_name="%(app_label)s_%(class)s_Kat_Senstivity",
        blank=True,
        null=True,
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name=_("Unit"),
        related_name="%(app_label)s_%(class)s_Unit",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{str(self.specimen_parameter_technique)}->{str(self.kat)}"

    @property
    def slug(self):
        return self.__str__

    class Meta:
        unique_together = [["kat", "specimen_parameter_technique"]]
        verbose_name = _("Specimen Parameter Technique Kat")
        verbose_name_plural = _("Specimen Parameter Technique Kats")
