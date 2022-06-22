from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from djongo.models import ArrayReferenceField
from polymorphic.models import PolymorphicModel
from GraphQL.models import BaseModel, BaseModelName
from GraphQL.custom_fields import QRField
from Facilities.models import Branch, Shift
from Persons.models import Doctor, Employee, Gender, Patient
from Products.models import Brand, LineInInvoice, MedicalSupply, Unit


# Create your models here.

class LabShift(Shift):  # شفتات ايام الاسبوع

    class Meta:
        verbose_name = _("Laboratory Shift")
        verbose_name_plural = _("Laboratory Shifts")

        
class LabEmployee(Employee):

    laboratory_shifts = models.ManyToManyField(
        LabShift,
        verbose_name=_("Laboratory Shift"),
        related_name="%(app_label)s_%(class)s_Laboratory_Shift",
    )
    
    class Meta:
        verbose_name = _("Laboratory Employee")
        verbose_name_plural = _("Laboratory Employees")


# TODO Employee Attendance Management System
## https://itsourcecode.com/uml/employee-attendance-management-system-er-diagram-erd/


class LaboratoryAttendance(models.Model):  # الحضور والغياب

    laboratory_employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=_("Laboratory Employee"),
        related_name="%(app_label)s_%(class)s_Laboratory_Employee",
    )
    laboratory_shift = models.ForeignKey(
        Shift,
        on_delete=models.CASCADE,
        verbose_name=_("Laboratory Shift"),
        related_name="%(app_label)s_%(class)s_Laboratory_Shift",
    )
    _date = models.DateField(
        auto_now=True,
        verbose_name=_("Date"),
    )

    @property
    def duration(self):
        attend = self.

        if()
        return 

    class Meta:
        unique_together = (
            "laboratory_employee",
            "laboratory_shift",
        )
        verbose_name = _("Laboratory Attendance")
        verbose_name_plural = _("Laboratory Attendances")


class LabSupply(MedicalSupply):
    
    class Meta:
        verbose_name = _("Laboratory Supply")
        verbose_name_plural = _("Laboratories Supplies")


class Stock(BaseModel):  # المخزون
    lab_supply = models.OneToOneField(
        LabSupply,
        on_delete=models.CASCADE,
        verbose_name=_("Laboratory Supply"),
    )
    # TODO PRODUCT DEATAILS STOCK
    product_details = models.ManyToManyField(
        LineInInvoice,
        verbose_name=_("Product Details"),
        related_name="%(app_label)s_%(class)s_Product_Details",
    )

    @property
    def packing(self):
        return self.lab_supply.default_packing

    @property  # inventory  المخزون
    def stock(self):
        return sum(list(map(lambda x: x["count_packing"], self.product_details)))

    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")

    def __str__(self):
        return str(self.product)

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class ShortCut(BaseModelName):
    
    class Meta:
        verbose_name = _("ShortCut")
        verbose_name_plural = _("ShortCuts")


class BodyLiquid(BaseModelName):
    genders = models.ManyToManyField(
        Gender,
        verbose_name=_("Genders"),
        related_name="%(app_label)s_%(class)s_Genders",
    )

    class Meta:
        verbose_name = _("BodyLiquid")
        verbose_name_plural = _("BodyLiquids")


class AnalyticalTechnique(BaseModelName):

    class Meta:
        verbose_name = _("Technique Method")
        verbose_name_plural = _("Technique Methods")


class ENeedNormal(models.Model):
    normal_range = models.ManyToManyField(
        NREntity,
        verbose_name=_("Normal Range"),
        through="NormalRange",
        related_name="%(app_label)s_%(class)s_Normal_Range",
    )

    class Meta:
        verbose_name = _("ENeed Normal")
        verbose_name_plural = _("ENeed Normals")


# TODO Duration Sample
class Sample(BaseModelName):
    
    class Action(models.TextChoices):
        Prandial = "Prandial"
        
    comments = models.TextField(
        max_length=200,
        verbose_name=_("Comments"),
    )
    time = models.TimeField(
        blank=True,
        null=True,
        verbose_name=_("Time"),
    )
    action_binding = models.CharField(max_length=20, verbose_name=_("Action Binding"), choices=Action.choices,blank=True, null=True,)
    duration_action = models.DurationField(
        blank=True,
        null=True,
        verbose_name=_("Duration Action"),
    )
    bodyLiquid = models.ForeignKey(BodyLiquid, on_delete=models.CASCADE, verbose_name=_("BodyLiquid"), related_name="%(app_label)s_%(class)s_BodyLiquid",)


    class Meta:
        verbose_name = _("Sample")
        verbose_name_plural = _("Samples")


class Parameter(BaseModelName):
    
    shortCuts = models.ManyToManyField(
        ShortCut,
        verbose_name=_("ShortCuts"),
        related_name="%(app_label)s_%(class)s_ShortCuts",
    )
    units = models.ManyToManyField(Unit, verbose_name=_("Units"), through="ParameterUnit", related_name="%(app_label)s_%(class)s_Units",)
    bodyLiquid = models.ManyToManyField(BodyLiquid, verbose_name=_("BodyLiquid"), through="BodyLiquidParameter", related_name="%(app_label)s_%(class)s_BodyLiquid",)
    # TODO CHEMICAL STRCTURE
    molecular_weight = models.SmallIntegerField(blank=True, null=True, verbose_name=_("Molecular Weight"))

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


class AnalyticalMethod(models.Model):
    class AnalyticalMethods(models.TextChoices):
        Qualitative = "Qualitative"
        SemiQuantitative = "Semi Quantitative"
        Quantitative = "Quantitative"

    name = models.CharField(max_length=20, verbose_name=_("Name"), choices=AnalyticalMethods.choices,)

    def __str__(self):
        return self.name

    def slug(self):
        return slugify(self.__str__)

    class Meta:
        verbose_name = _("Analytical Method")
        verbose_name_plural = _("Analytical Methods")


class BodyLiquidParameter(models.Model):
    bodyLiquid = models.ForeignKey(BodyLiquid, on_delete=models.CASCADE, verbose_name=_("BodyLiquid"), related_name="%(app_label)s_%(class)s_BodyLiquid",)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name=_("Parameter"), related_name="%(app_label)s_%(class)s_Parameter",)
    analytical_method = models.ManyToManyField(AnalyticalMethod, verbose_name=_("Analytical Method"), through="BodyLiquidParameterAnalyticalMethod", related_name="%(app_label)s_%(class)s_AnalyticalMethod",)
    
    def __str__(self):
        return f"{self.bodyLiquid}->{self.parameter}"

    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [["bodyLiquid", "parameter"]]
        verbose_name = _("BodyLiquid Parameter")
        verbose_name_plural = _("BodyLiquid Parameters")


class BodyLiquidParameterAnalyticalMethod(models.Model):
    bodyLiquid_parameter = models.ForeignKey(BodyLiquidParameter, on_delete=models.CASCADE, verbose_name=_("BodyLiquid Parameter"), related_name="%(app_label)s_%(class)s_BodyLiquid_Parameter",)
    analytical_method = models.ForeignKey(AnalyticalMethod, on_delete=models.CASCADE, verbose_name=_("Analytical Method"), related_name="%(app_label)s_%(class)s_Analytical_Method",)

    def __str__(self):
        return f"{self.bodyLiquid_parameter}->{self.analytical_method}"

    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [["bodyLiquid_parameter", "analytical_method"]]
        verbose_name = _("BodyLiquid Parameter Analytical Method")
        verbose_name_plural = _("BodyLiquid Parameter Analytical Methods")


class KatSensitivity(models.Model):
    low_sensitivity = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True, verbose_name=_("Low Sensitivity"), )
    high_sensitivity = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True, verbose_name=_("High Sensitivity"), )

    def __str__(self):
        return f"{self.low_sensitivity}->{self.high_sensitivity}"

    class Meta:
        verbose_name = _("Kat Sensitivity")
        verbose_name_plural = _("Kat Sensitivities")


class Analyzer(LabSupply):
    class Analyzers(models.TextChoices):
        HematolgyAnalyzer = "HematolgyAnalyzer"
        ElectrolyteAnalyzer = "ElectrolyteAnalyzer"
        UrineAnalyzer = "UrineAnalyzer"
        ChemistryAnalyzer = "ChemistryAnalyzer"

    type = models.CharField(max_length=20, verbose_name=_("Type"), choices=Analyzers.choices,)
    brochu_url = models.FileField(
        upload_to="Analyzers/",
        verbose_name=_("Brouchu URL"),
        null=True,
        blank=True,
    )
    test_volume = models.DecimalField(
        max_digits=2,
        decimal_places=2,
        verbose_name=_("Test Volume"),   
    )
    technique_method = models.ManyToManyField(
        TechniqueMethod,        
        verbose_name=_("Technique Method"),
        related_name="%(app_label)s_%(class)s_Technique_Method",
    )

    class Meta:
        verbose_name = _("Analyzer")
        verbose_name_plural = _("Analyzers")


class ClosedSystemAnalyzer(Analyzer):

    class Meta:
        verbose_name = _("Closed System Analyzer")
        verbose_name_plural = _("Closed System Analyzers")
 

class Kat(LabSupply):
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        verbose_name=_("Parameter"),
        related_name="%(app_label)s_%(class)s_Parameter",
    )
    samples = models.ManyToManyField(
        Sample,
        through="KatSample",
        verbose_name=_("Samples"),
        related_name="%(app_label)s_%(class)s_Samples",
    )
    technique_method = models.ForeignKey(TechniqueMethod, on_delete=models.CASCADE, verbose_name=_("Technique Method"), related_name="%(app_label)s_%(class)s_Technique_Method",)
        
    class Meta:
        verbose_name = _("Kat")
        verbose_name_plural = _("Kats")


class QualitativeKat(Kat):

    class Meta:
        verbose_name = _("Qualitative Kat")
        verbose_name_plural = _("Qualitative Kats")


class QuantitativeKat(Kat):
    normal_range = models.ForeignKey(ENeedNormal, on_delete=models.CASCADE, verbose_name=_("Normal range"), related_name="%(app_label)s_%(class)s_Normal_range",)
    kat_sensitivity = models.ForeignKey(KatSensitivity, on_delete=models.CASCADE, verbose_name=_("Kat Sensitivity"), related_name="%(app_label)s_%(class)s_Kat_Sensitivity",blank=True, null=True,)
    used_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name=_("Used Unit"),
        related_name="%(app_label)s_%(class)s_Used_Unit",
    )

    class Meta:
        verbose_name = _("Quantitative Kat")
        verbose_name_plural = _("Quantitative Kats")


class OpenSystemKat(QuantitativeKat):

    class Meta:
        verbose_name = _("Open System Kat")
        verbose_name_plural = _("Open System Kats")


class ClosedSystemKat(QuantitativeKat):
    analyzer = models.ForeignKey(ClosedSystemAnalyzer, on_delete=models.CASCADE, verbose_name=_("Closed System Analyzer"), related_name="%(app_label)s_%(class)s_Closed_System_Analyzer",)
    start_up_consumption = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True, verbose_name=_("Start Up Consumption"),) # استهلاك الكيمويات فى فتح الجهاز
    test_consumption = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True, verbose_name=_("Test Consumption"),) # استهلاك الكيمويات لتحليل
    end_consumption = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True, verbose_name=_("End Consumption"),) # استهلاك الكيمويات فى غلق الجهاز

    class Meta:
        verbose_name = _("Closed System Kat")
        verbose_name_plural = _("Closed System Kats")


class Standard(models.Model):
    serial = models.CharField(max_length=20, primary_key=True, verbose_name=_("Serial No."),)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_("Brand"), related_name="%(app_label)s_%(class)s_Brand",)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, verbose_name=_("Parameter"), related_name="%(app_label)s_%(class)s_Parameter",)
    concentration = models.DecimalField(max_digits=3, decimal_places=2, verbose_name=_("Concentration"),)

    def __str__(self):
        return f"{str(self.brand)}->{str(self.parameter)}"

    @property
    def slug(self):
        return self.__str__

    class Meta:
        verbose_name = _("Standard")
        verbose_name_plural = _("Standards")


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
    is_favorite = models.BooleanField(default=True, verbose_name=_("Is favorite"),)

    def __str__(self):
        return f"{str(self.kat)}->{str(self.sample)}"

    @property
    def slug(self):
        return self.__str__

    class Meta:
        unique_together = [["kat", "sample"]]
        verbose_name = _("Kat Sample")
        verbose_name_plural = _("Kat Samples")


# class QualitativeBodyLiquidParameter(BodyLiquidParameter):

#     class Meta:
#         verbose_name = _("Qualitative BodyLiquid Parameter")
#         verbose_name_plural = _("Qualitative BodyLiquid Parameters")


# class QuantitativeBodyLiquidParameter(BodyLiquidParameter):
#     minimum_value = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True, verbose_name=_("Minimum Value"), )
#     maximum_value = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True, verbose_name=_("Maximum Value"), )
#     units = models.ManyToManyField(
#         Unit,
#         through="SampleParameterUnit",
#         verbose_name=_("Units"),
#     )

#     class Meta:
#         verbose_name = _("Quantitative BodyLiquid Parameter")
#         verbose_name_plural = _("Quantitative BodyLiquid Parameters")


# NOTE Bind with Medicin
class DisksAntiBiotic(Kat):
    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_("Code"),
    )
    for_child_pregnant = models.BooleanField(
        default=True,
        verbose_name=_("for Child / Pregnant"),
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("Disks Anti-Biotic")
        verbose_name_plural = _("Disks Anti-Biotics")


class RunedParameter(QuantitativeSampleParameter):
    samples = models.ManyToManyField(
        Sample,
        through="SampleRunedParameter",
        verbose_name=_("Samples"),
        related_name="%(app_label)s_%(class)s_Samples",
    )

    class Meta:
        verbose_name = _("Runed Parameter")
        verbose_name_plural = _("Runed Parameters")


class CalculatedParameter(QuantitativeSampleParameter):
    equation_parameter = models.ManyToManyField(RunedParameter, verbose_name=_("Equation Parameter"), through="EquationParameter", related_name="%(app_label)s_%(class)s_Equation_Parameter",)
    equation = models.CharField(max_length=20, verbose_name=_("Equation"),)
    
    class Meta:
        verbose_name = _("Calculated Parameter")
        verbose_name_plural = _("Calculated Parameters")



class EquationParameter(models.Model):
    calculated_parameter = models.ForeignKey(CalculatedParameter, on_delete=models.CASCADE, verbose_name=_("Calculated Parameter"), related_name="%(app_label)s_%(class)s_Calculated_Parameter",)
    related_runed_parameter = models.ForeignKey(RunedParameter, on_delete=models.CASCADE, verbose_name=_("Related Runed Parameter"), related_name="%(app_label)s_%(class)s_Related_Runed_Parameter",)
    symbol_in_equation = models.CharField(max_length=1, verbose_name=_("Symbol in Equation"))

    def __str__(self):
        return f"{str(self.calculated_parameter)}->{str(self.related_runed_parameter)}"

    @property
    def slug(self):
        return self.__str__

    class Meta:
        uniqe_together = [["calculated_parameter", "related_runed_parameter"]]
        verbose_name = _("Equation Parameter")
        verbose_name_plural = _("Equation Parameters")


class BlockOfAnalysis(PolymorphicModel):  # Generalization for Price And ShortCut
    shortcuts = ArrayReferenceField(
        to=ShortCut,
        on_delete=models.CASCADE,
        verbose_name=_("Shortcuts"),
        related_name="%(app_label)s_%(class)s_Shortcuts",
    )
    price_for_patient = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Price For Patient"),
    )
    price_for_laboratories = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Price For Laboratories"),
    )
    lab_2_lab = models.ManyToManyField(
        MainLab,
        through="MainLabMenu",
        verbose_name=_("Lab To Lab"),
    )

    class Meta:
        verbose_name = _("Block Of Analysis")
        verbose_name_plural = _("Block Of Analysis")


class Package(BaseModelName, BlockOfAnalysis):
    analysis_in_package = models.ManyToManyField(
        BlockOfAnalysis,
        verbose_name=_("Analysis in Package"),
        related_name="%(app_label)s_%(class)s_Belng_To_Report",
    )

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")


class Report(BaseModelName, BlockOfAnalysis):

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")


class Function(BaseModelName, BlockOfAnalysis):
    belong_to_report = models.ForeignKey(
        Report,
        verbose_name=_("Belng To Report"),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_Belng_To_Report",
    )

    class Meta:
        verbose_name = _("Function")
        verbose_name_plural = _("Functions")


class GroupAnalysis(BaseModelName, BlockOfAnalysis):
    belong_to_function = models.ForeignKey(
        Function,
        verbose_name=_("Belng To Function"),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_Belng_To_Function",
    )

    class Meta:
        verbose_name = _("Group Analysis")
        verbose_name_plural = _("Group Analysis")


class NormalRange(models.Model):
    n_r_entity = models.ForeignKey(
        NREntity,
        verbose_name=_("N R Entity"),
        related_name="%(app_label)s_%(class)s_N_R_Entity",
    )
    e_need_normal = models.ForeignKey(
        ENeedNormal,
        verbose_name=_("E Need Normal"),
        related_name="%(app_label)s_%(class)s_E_Need_Normal",
    )

    low_normal = models.DecimalField(max_digits=2, decimal_places=2)
    high_normal = models.DecimalField(max_digits=2, decimal_places=2)

    class Meta:
        verbose_name = _("Normal Range")
        verbose_name_plural = _("Normal Ranges")


class Analysis(BlockOfAnalysis):
    sample_runed_parameter = models.ForeignKey(
        SampleRunedParameter,
        on_delete=models.CASCADE,
        verbose_name=_("Sample Runed Parameter"),
        related_name="%(app_label)s_%(class)s_Sample_Runed_Parameter",
    )
    technique_method = models.ForeignKey(
        AnalyticalTechnique,
        on_delete=models.CASCADE,
        verbose_name=_("Technique Method"),
        related_name="%(app_label)s_%(class)s_Technique_Method",
    )    
    normal_range = models.ForeignKey(
        ENeedNormal,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_Normal_Range",
        verbose_name=_("Normal Range"),
        blank=True,
        null=True,
    )
    belong_to = models.ManyToManyField(
        BlockOfAnalysis,
        verbose_name=_("Belong To"),
        related_name="%(app_label)s_%(class)s_Belong_To",
    )
    is_default = models.BooleanField(
        default=True,
        verbose_name=_("is Default"),
    )
    is_available = models.BooleanField(
        default=True,
        verbose_name=_("is Available"),
    )
    is_constant_for_patient = models.BooleanField(default = False, verbose_name=_("Is Constant for Pateint"),)

    def __str__(self):
        return (
            f"{str(self.sample_runed_parameter)}->{str(self.technique_method)}"
        )

    @property
    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [
            [
                "sample_runed_parameter",
                "technique_method",
            ]
        ]
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

    analysis_shortCut = models.ForeignKey(
        BlockOfAnalysis,
        on_delete=models.CASCADE,
        verbose_name=_("Analysis ShortCut"),
    )
    laboratory = models.ForeignKey(
        MainLab,
        on_delete=models.CASCADE,
        verbose_name=_("Laboratory"),
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
        related_name="%(app_label)s_%(class)s_normal_range",
        verbose_name=_("Normal Range"),
        blank=True,
        null=True,
    )
    is_default = models.BooleanField(
        default=True,
        verbose_name=_("is Default"),
    )

    def __str__(self):
        return f"{str(self.analysis_shortCut)}->{str(self.laboratory)}"

    @property
    def slug(self):
        return slugify(f"{str(self.analysis_shortCut)}->{str(self.laboratory)}")

    class Meta:
        unique_together = [
            [
                "analysis_shortCut",
                "laboratory",
            ]
        ]
        verbose_name = _("Main Lab Menu")
        verbose_name_plural = _("Main Lab Menus")


class BloodGroup(BaseModelName):  # ENUM
    class ABOSystem(models.TextChoices):
        A = "A"
        B = "B"
        AB = "AB"
        O = "O"

    class Rh_Type(models.TextChoices):
        Positive = "Positive"
        Negative = "Negative"

    ABO_system = models.CharField(
        max_length=2,
        choices=ABOSystem.choices,
        verbose_name=_("ABO System"),
    )
    Rh_type = models.CharField(
        max_length=8,
        choices=Rh_Type.choices,
        verbose_name=_("Rh Type"),
    )

    class Meta:
        unique_together = (
            "ABO_system",
            "Rh_type",
        )
        verbose_name = _("Blood Group")
        verbose_name_plural = _("Blood Groups")


class Senstivity(models.Model):  # ENUM
    class Senstive(models.TextChoices):
        Strong = "Strong"
        Mmderate = "Moderate"
        weak = "Weak"
        very_weak = "Very Weak"

    name = models.CharField(
        max_length=10,
        primary_key=True,
        choices=Senstive.choices,
        verbose_name=_("Name"),
    )

    def __str__(self):
        return str(self.name)

    @property
    def slug(self):
        return slugify(self.name)

    class Meta:
        verbose_name = _("Senstivity")
        verbose_name_plural = _("Senstivites")


class HighLow(models.Model):  # ENUM
    class HL(models.TextChoices):
        high = "High"
        low = "Low"

    name = models.CharField(
        max_length=5,
        primary_key=True,
        choices=HL.choices,
        verbose_name=_("Name"),
    )

    def __str__(self):
        return str(self.name)

    @property
    def slug(self):
        return slugify(self.name)

    class Meta:
        verbose_name = _("High or Low")
        verbose_name_plural = _("High or Low")


class LabDepartement(BaseModelName):
    class Meta:
        verbose_name = _("Lab Departement")
        verbose_name_plural = _("Lab Departements")


#  🧕   🕌   🕋  👳  💲  🌍  👰‍♂️   👰‍♀️   👩‍❤️‍💋‍👩   🤰🏻   🏋️‍♀️   💒   👩‍❤️‍💋‍👨   🧑🏼‍🍼  👩‍🎓   🚣‍♀️  🤾‍♀️  👨‍💼   👷🏽‍♂️  👷🏼‍♀️   👨‍🔧   👨‍⚕  👩🏽‍⚕️  👨🏻‍🎓  👨🏼‍🏫  👩🏽‍🏫   🦷


class VitalSign(BaseModelName):
    # TODO Normal Range
    normal_range = models.ForeignKey(
        ENeedNormal,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_normal_range",
        verbose_name=_("Normal Range"),
        blank=True,
        null=True,
    )
    unit = models.ForeignKey(
        Unit,
        verbose_name=_("Unit"),
        on_delete=models.CASCADE,
        related_name=_("%(app_label)s_%(class)s_Unit"),
        blank=True,
        null=True,
    )

    """
    vital and sign*
    patient and observation*
    patient and monitoring Second search terms include:
    heart rate AND (determin* OR measure*)
    blood pressure AND (determin* OR measure*)
    body temperature AND (determin* OR measure*)
    respiratory rate AND (determin* OR measure*)
    vital signs AND (determin* OR measure*)
    fifth vital sign AND (determin* OR measure*)
    monitoring AND physiological AND/OR nursing
    pulse AND evaluat*
    pulse oximetry AND (determin* OR measure*)
    patient oxygenation AND (determin* OR measure*)
    pain AND vital sign (determin* OR measure*)
    blood and pressure in ti
    respirat* in ti
    pulse in ti
    temperature in ti
    vital and sign* in ti
    observation* in ti.
    fasting. / postprandial

    حيوية وعلامة *
    المريض والمراقبة *
    تتضمن مصطلحات البحث الثانية الخاصة بالمريض والمراقبة ما يلي:
    معدل ضربات القلب و (تحديد * أو قياس *)
    ضغط الدم و (تحديد * أو قياس *)
    درجة حرارة الجسم و (تحديد * أو قياس *)
    معدل التنفس و (تحديد * أو قياس *)
    العلامات الحيوية و (تحديد * أو قياس *)
    العلامة الحيوية الخامسة AND (تحديد * أو قياس *)
    المراقبة و / أو الفسيولوجية و / أو التمريض
    نبض وتقييم *
    قياس النبض و (تحديد * أو قياس *)
    أكسجة المريض و (تحديد * أو قياس *)
    الألم والعلامة الحيوية (تحديد * أو قياس *)
    الدم والضغط في تي
    تنفس * في ti
    نبض في ti
    درجة الحرارة في تي
    الحيوية وتسجيل الدخول ti
    المراقبة * في ti
    صاءم او فاطر
    """

    class Meta:
        verbose_name = _("Vital Sign")
        verbose_name_plural = _("Vital Signs")


class Run(models.Model):
    start = models.DateTimeField(auto_now_add=True, verbose_name=_(""))
    def __str__(self):
        return str(self.id)

    @property
    def slug(self):
        return slugify(self.__str__)

    class Meta:
        verbose_name = _("Run")
        verbose_name_plural = _("Runs")


class Visit(BaseModel):
    # TODO BarCode QR FEILD
    qr = QRField(verbose_name=_("Visit QR"))
    # qr = models.UUIDField(
    #     primary_key=True,
    #     default=uuid.uuid4,
    #     editable=False,
    #     verbose_name=_("QR"),
    # )
    # id = models.BigAutoField(primary_key=True)

    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name=_("Branch"),
        related_name=_("%(app_label)s_%(class)s_Branch"),
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        verbose_name=_("Patient"),
        related_name=_("%(app_label)s_%(class)s_Patient"),
    )

    treating_doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        verbose_name=_("Treating Doctor"),
        related_name=_("%(app_label)s_%(class)s_Treating_Doctor"),
        blank=True,
        null=True,
    )
    visit_patient_vitalSigns = models.ManyToManyField(
        VitalSign,
        through="VisitPatientVitalSign",
        verbose_name=_("Visit Patient Vital Signs"),
    )
    Required_blocks_of_analysis = models.ManyToManyField(
        BlockOfAnalysis,
        through="VisitBlockOfAnalysis",
        verbose_name=_("Required Blocks Of Analysis"),
        related_name=_("%(app_label)s_%(class)s_Blocks_Of_Analysis"),
    )
    # run = models.ManyToManyField(
    #     Run,
    #     through="VisitBlockOfAnalysis",
    #     verbose_name=_("Run"),
    #     related_name=_("%(app_label)s_%(class)s_Run"),
    # )

    # TODO Employee Activity
    lab_employee_activity = models.ManyToManyField(
        LabEmployee,
        through="LabEmployeeActivity",
        verbose_name=_("Lab Employee Activity"),
    )

    # TODO الحسابات
    # TODO الاستهلاك من المخزن

    def __str__(self):
        return f"{str(self.branch)}->{str(self.patient)}->{str(self.create_at)}"

    @property
    def slug(self):
        return slugify(
            f"{str(self.branch)}->{str(self.patient)}->{str(self.create_at)}"
        )

    class Meta:
        unique_together = [["patient", "branch", "create_at"]]
        verbose_name = _("Visit")
        verbose_name_plural = _("Visits")


############################################################################################################################################
class VisitBlockOfAnalysis(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        verbose_name=_("Visit"),
        related_name=_("%(app_label)s_%(class)s_Visit"),
    )
    block_of_analysis = models.ForeignKey(
        BlockOfAnalysis,
        on_delete=models.CASCADE,
        verbose_name=_("Block Of Analysis"),
        related_name=_("%(app_label)s_%(class)s_Block_Of_Analysis"),
    )
    run = models.ForeignKey(
        Run,
        on_delete=models.CASCADE,
        verbose_name=_("Run"),
        related_name=_("%(app_label)s_%(class)s_Run"),
    )

    def __str__(self):
        return f"{str(self.visit)}->{str(self.block_of_analysis)}"

    @property
    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [["visit", "block_of_analysis"]]
        verbose_name = _("Visit Block Of Analysis")
        verbose_name_plural = _("Visits Blocks Of Analysis")


############################################################################################################################################
class VisitReport(models.Model):
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        verbose_name=_("Visit"),
        related_name=_("%(app_label)s_%(class)s_Visit"),
    )
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        verbose_name=_("Report"),
        related_name=_("%(app_label)s_%(class)s_Report"),
    )
    group_in_visit_report = models.ManyToManyField(
        GroupAnalysis,
        through="Group In Visit Report",
        verbose_name=_("Group In Visit Report"),
        related_name=_("%(app_label)s_%(class)s_Group_In_Visit_Report"),
    )

    def __str__(self):
        return f"{str(self.visit)}->{str(self.report)}"

    @property
    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [["visit", "report"]]
        verbose_name = _("Visit Report")
        verbose_name_plural = _("Visits Reports")


class GroupInVisitReport(models.Model):
    visit_report = models.ForeignKey(
        VisitReport,
        on_delete=models.CASCADE,
        verbose_name=_("VisitReport"),
        related_name=_("%(app_label)s_%(class)s_VisitReport"),
    )
    group_analysis = models.ForeignKey(
        GroupAnalysis,
        on_delete=models.CASCADE,
        verbose_name=_("Group Analysis"),
        related_name=_("%(app_label)s_%(class)s_Group_Analysis"),
    )
    line_in_report = models.ManyToManyField(
        Analysis,
        through="LineInReport",
        verbose_name=_("Line In Report"),
        related_name=_("%(app_label)s_%(class)s_Line_In_Report"),
    )

    def __str__(self):
        return f"{str(self.visit_report)}->{str(self.group_analysis)}"

    @property
    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [["visit_report", "group_analysis"]]
        verbose_name = _("Group In Report")
        verbose_name_plural = _("Groups In Reports")


class LineInReport(models.Model):
    group_in_report = models.ForeignKey(
        GroupInVisitReport,
        on_delete=models.CASCADE,
        verbose_name=_("Group In Report"),
        related_name=_("%(app_label)s_%(class)s_Group_In_Report"),
    )
    analysis = models.ForeignKey(
        Analysis,
        on_delete=models.CASCADE,
        verbose_name=_("Analysis"),
        related_name=_("%(app_label)s_%(class)s_Analysis"),
    )
    value = 
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name=_("Unit"),
        related_name=_("%(app_label)s_%(class)s_Unit"),
    )
    normal_range = models.ForeignKey(
        NormalRange,
        on_delete=models.CASCADE,
        verbose_name=_("Unit"),
        related_name=_("%(app_label)s_%(class)s_Unit"),
    )

    @property
    def unit(self):
        return self.analysis.unit

    def __str__(self):
        return f"{str(self.group_in_report)}->{str(self.analysis)}"

    @property
    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [["group_in_report", "analysis"]]
        verbose_name = _("Line In Report")
        verbose_name_plural = _("Lines In Reports")


############################################################################################################################################


class VisitPatientVitalSign(models.Model):  # المؤشرات الحيويه للمريض
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        verbose_name=_("Visit"),
        related_name=_("%(app_label)s_%(class)s_Visit"),
    )
    vitalSign = models.ForeignKey(
        VitalSign,
        on_delete=models.CASCADE,
        verbose_name=_("Vital Sign"),
        related_name=_("%(app_label)s_%(class)s_Vital_Sign"),
    )
    value = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name=_("Value"),
    )

    def __str__(self):
        return f"{str(self.visit)}->{str(self.vitalSign)}"

    @property
    def slug(self):
        return slugify(f"{str(self.visit)}->{str(self.vitalSign)}")

    class Meta:
        unique_together = [["visit", "vitalSign"]]
        verbose_name = _("Visit Patient Vital Sign")
        verbose_name_plural = _("Visit Patient Vital Signs")


class LabEmployeeActivity(models.Model):
    class Activity(models.TextChoices):
        Print = "Print"

    lab_employee = models.ForeignKey(
        LabEmployee,
        on_delete=models.CASCADE,
        verbose_name=_("Lab Employee"),
        related_name=_("%(app_label)s_%(class)s_Lab_Employee"),
    )
    visit = models.ForeignKey(
        Visit,
        on_delete=models.CASCADE,
        verbose_name=_("Visit"),
        related_name=_("%(app_label)s_%(class)s_Visit"),
    )
    activity = models.CharField(
        max_length=5,
        choices=Activity.choices,
        verbose_name=_("Activity"),
    )
    execution_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Execution Time"),
    )

    def __str__(self):
        return f"{str(self.lab_employee)}->{str(self.visit)}"

    @property
    def slug(self):
        return slugify(f"{str(self.lab_employee)}->{str(self.visit)}")

    class Meta:
        unique_together = [["lab_employee", "visit", "activity"]]
        verbose_name = _("Lab Employee Activity")
        verbose_name_plural = _("Lab Employee Activitys")
