from django.db import models
from polymorphic.models import PolymorphicModel
from GraphQL.models import BaseModel, BaseModelLogo, BaseModelName
from Location.models import Country
from Facilities.models import Compony
from Persons.models import Customer, Employee
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from quantityfield.fields import (
    QuantityField,
    IntegerQuantityField,
    BigIntegerQuantityField,
    DecimalQuantityField,
)

from django_prices.models import MoneyField, TaxedMoneyField


# from django_measurement.models import MeasurementField
# from measurement.measures import Volume

# Create your models here.


class Unit(BaseModelName):
    units_related = models.ManyToManyField(
        "self",
        through="UnitConvert",
        symmetrical=False,
        verbose_name=_("Units Related"),
    )

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class UnitConvert(models.Model):
    from_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name=_("from Unit"),
    )
    to_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_unit_convert",
        verbose_name=_("to Unit"),
    )
    factor = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        verbose_name=_("Factor"),
    )

    def __str__(self):
        return f"{self.from_unit} -> {self.to_unit}"

    class Meta:
        unique_together = [["from_unit", "to_unit"]]
        verbose_name = _("Unit Convert")
        verbose_name_plural = _("Unit Converts")


class Brand(BaseModelLogo):
    made_in = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name=_("Made In"),
    )

    class Meta:
        verbose_name = _("Unit")
        verbose_name_plural = _("Units")


class MainCategory(BaseModelName):
    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")


class SubCategory(BaseModelName):
    main_category = models.ForeignKey(
        MainCategory,
        on_delete=models.CASCADE,
        verbose_name=_("Main Category"),
    )

    class Meta:
        verbose_name = _("Sub Category")
        verbose_name_plural = _("Sub Categorys")


class Product(PolymorphicModel, BaseModelName, BaseModel):  # Weak Entity
    class Packing(models.TextChoices):
        Package = "Package"

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name=_("Brand"),
    )
    image_url = models.ImageField(
        upload_to="images/Products/",
        verbose_name=_("Image URL"),
    )
    serial = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Serial No"),
    )
    category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        verbose_name=_("Category"),
    )
    default_packing = models.CharField(
        max_length=10,
        choices=Packing.choices,
        verbose_name=_("Default Packing"),
    )
    package_size = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name=_("Package Size"),
    )
    measurment_unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        verbose_name=_("Measurment Unit"),
    )

    class Meta:
        unique_together = (
            "name",
            "brand",
        )
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class Invoice(models.Model):
    products = models.ManyToManyField(
        Product,
        through="LineInInvoice",
        verbose_name=_("Products"),
    )
    employee_recipient = models.ForeignKey(
        Employee,
        on_delete=models.SET("Deleted"),
        verbose_name=_("Employee Recipient"),
    )  # موظف الاستقبال
    supplier = models.ForeignKey(
        Compony,
        on_delete=models.SET("Deleted"),
        verbose_name=_("Supplier"),
    )
    received_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Received Date"),
    )

    @property
    def total_price(self):
        return sum(map(lambda x: x["total_price"], self.products))

    currency = models.CharField(max_length=3, default="BTC")
    price_net_amount = models.DecimalField(max_digits=9, decimal_places=2, default="5")
    price_net = MoneyField(amount_field="price_net_amount", currency_field="currency")
    price_gross_amount = models.DecimalField(
        max_digits=9, decimal_places=2, default="5"
    )
    price_gross = MoneyField(
        amount_field="price_gross_amount", currency_field="currency"
    )
    price = TaxedMoneyField(
        net_amount_field="price_net_amount",
        gross_amount_field="price_gross_amount",
        currency="currency",
    )

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")


class LineInInvoice(models.Model):  #  Many to Many RealtionShip Product + Invoice
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        verbose_name=_("Invoice"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_product",
        verbose_name=_("Product"),
    )
    # packing = models.ForeignKey(
    #     Product,
    #     on_delete=models.CASCADE,
    #     to_field="default_packing",
    # )
    packing_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Packing Price"),
    )
    expire_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Expire Date"),
    )
    count_packing = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Count Packing"),
    )

    @property
    def total_price(self):
        return self.packing_price * self.count_packing

    class Meta:
        unique_together = [
            [
                "invoice",
                "product",
            ]
        ]
        verbose_name = _("Line In Invoice")
        verbose_name_plural = _("Lines In Invoice")


# TODO


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_("Customer"),
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name=_("Employee"),
    )
    order_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Order Date"),
    )
    required_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Required Date"),
    )
    shipped_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Shipped Date"),
    )
    total_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Total Price"),
    )
    comment = models.TextField(
        max_length=300,
        verbose_name=_("Comment"),
    )
    products = models.ManyToManyField(
        Product,
        through="ProductOrder",
        verbose_name=_("Products"),
    )

    # Invoice_Number	Charge or Cash Invoice Number	Int	11
    # OR_Number	Official Receipt Number	Int	11
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")


class ProductOrder(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Order"),
    )
    quantity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Quantity"),
    )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Price"),
    )

    # TODO packing
    @property
    def packing(self):
        return self.product.packing

    @property
    def total_price(self) -> float:
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product}-{self.order}"

    class Meta:
        unique_together = [
            [
                "product",
                "order",
            ]
        ]
        verbose_name = _("Product Order")
        verbose_name_plural = _("Product Orders")


class Deal(PolymorphicModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name=_("Order"),
    )
    # Invoice_Number	Charge or Cash Invoice Number	Int	11
    down_payment = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Down Payment"),
    )  # دفعه قدمه
    rebate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Rebate"),
    )  # الخصم

    class Meta:
        verbose_name = _("Deal")
        verbose_name_plural = _("Deals")


class CashDeal(Deal):
    rebate_cash = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Rebate Cash"),
    )  #  خصم الكاش

    class Meta:
        verbose_name = _("Cash Deal")
        verbose_name_plural = _("Cash Deals")


class ChargeDeal(Deal):
    cost_charge = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Cost Charge"),
    )  # تكلفه الشحن

    class Meta:
        verbose_name = _("Charge Deal")
        verbose_name_plural = _("Charge Deals")
