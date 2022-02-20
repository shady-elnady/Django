from django.db import models
from djongo.models import ArrayReferenceField
from GraphQL.models import BaseModel, BaseModelName
from polymorphic.models import PolymorphicModel
from Facilities.models import Branch, MainLab
from Persons.models import Doctor, LabEmployee, NREntity, Patient
from Products.models import LineInInvoice, Product, Unit
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from GraphQL.custom_fields import QRField
import uuid


# Create your models here.


class Stock(BaseModel):  # المخزون
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
    )
    produuct_details = models.ManyToManyField(
        LineInInvoice,
        on_delete=models.CASCADE,
        verbose_name=_("Product Details"),
        related_name="%(app_label)s_%(class)s_Product_Details",
    )

    @property
    def packing(self):
        return self.product.default_packing

    @property  # inventory  المخزون
    def stock(self):
        return sum(list(map(lambda x: x["count_packing"], self.details)))

    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")

    def __str__(self):
        return str(self.product)

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class TechniqueMethod(BaseModelName):
    class Meta:
        verbose_name = _("Technique Method")
        verbose_name_plural = _("Technique Methods")


# TODO Duration Sample
class Sample(BaseModelName):
    class Action(models.TextChoices):
        Prandial = "Prandial"
    comment = models.TextField(
        max_length=200,
        verbose_name=_("Comment"),
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
    is_need_collection_tube = models.BooleanField(default=True, verbose_name=_("Is Need Collection Tube"))

    class Meta:
        verbose_name = _("Sample")
        verbose_name_plural = _("Samples")


class MedicalSupply(Product):

    class Meta:
        verbose_name = _("Medical Supply")
        verbose_name_plural = _("Medical Supplies")

        
class Kat(Product):
    
    class Meta:
        verbose_name = _("Kat")
        verbose_name_plural = _("Kats")


class Analyzer(Product):
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


class ClosedAnalyzer(Analyzer):
    kats = models.ManyToManyField(Kat , verbose_name=_("Kats"), through="KatAnalyzer",related_name="%(app_label)s_%(class)s_Kats",)

    class Meta:
        verbose_name = _("ClosedAnalyzer")
        verbose_name_plural = _("ClosedAnalyzers")


class KatClosedAnalyzer(models.Model):
    kat = models.ForeignKey(Kat, on_delete=models.CASCADE, verbose_name=_("Kat"), related_name="%(app_label)s_%(class)s_Kat",)
    closed_analyzer = models.ForeignKey(ClosedAnalyzer, on_delete=models.CASCADE, verbose_name=_("Closed Analyzer"), related_name="%(app_label)s_%(class)s_Closed_Analyzer",)
    start_up_consumption = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True, verbose_name=_("Start Up Consumption"),) # استهلاك الكيمويات فى فتح الجهاز
    test_consumption = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True, verbose_name=_("Test Consumption"),) # استهلاك الكيمويات لتحليل
    end_consumption = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True, verbose_name=_("End Consumption"),) # استهلاك الكيمويات فى غلق الجهاز
    
    class Meta:
        unique_together = [["kat", "closed_analyzer"]]
        verbose_name = _("Kat ClosedAnalyzer")
        verbose_name_plural = _("Kats ClosedAnalyzers")


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


class ShortCut(BaseModelName):
    class Meta:
        verbose_name = _("ShortCut")
        verbose_name_plural = _("ShortCuts")


class Parameter(BaseModelName):
    samples = models.ManyToManyField(
        Sample,
        through="SampleParameter",
        symmetrical=False,
        verbose_name=_("Samples"),
    )
    units = models.ManyToManyField(
        Unit,
        through="ParameterUnit",
        symmetrical=False,
        verbose_name=_("Units"),
    )

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
    is_default = models.BooleanField(
        default=True,
        verbose_name=_("is Default"),
    )
    parameter_unit_related = models.ManyToManyField(
        "self",
        through="ParameterUnitConvert",
        symmetrical=True,
        verbose_name=_("Parameter Unit Related"),
    )

    def __str__(self):
        return f"{self.parameter}->{self.unit}"

    @property
    def slug(self):
        return slugify(f"{self.parameter}->{self.unit}")

    class Meta:
        unique_together = [["parameter", "unit"]]
        verbose_name = _("Parameter Unit")
        verbose_name_plural = _("Parameter Units")


class ParameterUnitConvert(models.Model):
    from_parameter_unit = models.ForeignKey(
        ParameterUnit,
        on_delete=models.CASCADE,
        verbose_name=_("from Parameter Unit"),
    )
    to_parameter_unit = models.ForeignKey(
        ParameterUnit,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_parameter_unit_convert",
        verbose_name=_("to Parameter Unit"),
    )
    factor = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        verbose_name=_("Factor"),
    )

    def __str__(self):
        return f"{self.from_parameter_unit}->{self.to_parameter_unit}"

    @property
    def slug(self):
        return slugify(f"{self.from_parameter_unit}->{self.to_parameter_uni}")

    class Meta:
        unique_together = [["from_parameter_unit", "to_parameter_unit"]]
        verbose_name = _("Parameter Unit Convert")
        verbose_name_plural = _("Parameter Unit Converts")


class AnalyzerKatTechniqueMethod(models.Model):
    analyzer = models.ForeignKey(
        Analyzer,
        on_delete=models.CASCADE,
        verbose_name=_("Analyzer"),
    )
    kat_technique_method = models.ForeignKey(
        KatTechniqueMethod,
        on_delete=models.CASCADE,
        verbose_name=_("Kat Technique Method"),
    )

    def __str__(self):
        return f"{self.analyzer}->{self.kat_technique_method}"

    @property
    def slug(self):
        return slugify(f"{self.analyzer}->{self.kat_technique_method}")

    class Meta:
        unique_together = [["analyzer", "kat_technique_method"]]
        verbose_name = _("Analyzer Kat Technique Method")
        verbose_name_plural = _("Analyzer Kat Technique Methods")


class BlockOfAnalysis(PolymorphicModel):  # Generalization for Price And ShortCut
    shortcuts = ArrayReferenceField(
        to=ShortCut,
        on_delete=models.CASCADE,
        verbose_name=_("Shortcuts"),
        related_name="%(app_label)s_%(class)s_Shortcuts",
        blank=True,
        null=True,
    )
    price_patient = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Price Patient"),
    )
    price_lab = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Price Lab"),
    )
    lab_2_lab = models.ManyToManyField(
        MainLab,
        through="MainLabMenu",
        verbose_name=_("Lab to Lab"),
    )

    class Meta:
        verbose_name = _("Group ShortCut")
        verbose_name_plural = _("Group ShortCuts")


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


class SampleParameter(models.Model):
    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.CASCADE,
        verbose_name=_("Parameter"),
    )
    sample = models.ForeignKey(
        Sample,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Sample"),
    )

    group_analysis = models.ForeignKey(
        GroupAnalysis,
        verbose_name=_("Group Analysis"),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_Group_Analysis",
    )

    analyzer_kat_technique_method = models.ManyToManyField(
        AnalyzerKatTechniqueMethod,
        through="Analysis",
        verbose_name=_("analyzer Kat Technique Method"),
    )

    def __str__(self):
        return f"{self.sample}->{self.parameter}"

    @property
    def slug(self):
        return slugify(f"{self.sample}->{self.parameter}")

    class Meta:
        unique_together = [["parameter", "sample"]]
        verbose_name = _("Sample Parameter")
        verbose_name_plural = _("Sample Parameters")


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
    sample_parameter = models.ForeignKey(
        SampleParameter,
        on_delete=models.CASCADE,
        verbose_name=_("Sample Parameter"),
        related_name="%(app_label)s_%(class)s_Sample_Parameter",
    )
    analyzer_kat_technique_method = models.ForeignKey(
        AnalyzerKatTechniqueMethod,
        on_delete=models.CASCADE,
        verbose_name=_("Analyzer Kat Technique Method"),
        related_name="%(app_label)s_%(class)s_Analyzer_Kat_Technique_Method",
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
    group_analysis = models.ForeignKey(
        GroupAnalysis,
        verbose_name=_("Group Analysis"),
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_Group_Analysis",
        blank=True,
        null=True,
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
            f"{str(self.sample_parameter)}->{str(self.analyzer_kat_technique_method)}"
        )

    @property
    def slug(self):
        return slugify(self.__str__)

    class Meta:
        unique_together = [
            [
                "sample_parameter",
                "analyzer_kat_technique_method",
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
