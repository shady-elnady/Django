from django.db import models
from Facilities.models import Compony
from GraphQL.models import BaseModel, BaseModelName
from polymorphic.models import PolymorphicModel
from Location.models import Country
from Nady_System.models import Unit
from Persons.models import Customer, Employee
from djongo.models import ArrayReferenceField

# Create your models here.


class Brand(BaseModelName):
    made_in = models.ForeignKey(
        Country,
        related_name="brands",
        on_delete=models.CASCADE,
    )
    logo_url = models.CharField(max_length=100, null=True, blank=True)


class MainCategory(BaseModelName):
    pass


class SubCategory(BaseModelName):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)


class Product(PolymorphicModel, BaseModelName, BaseModel):  # Weak Entity
    class Packing(models.TextChoices):
        Package = "Package"

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="images")
    serial = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    default_packing = models.CharField(max_length=10, choices=Packing.choices)
    package_size = models.DecimalField(max_digits=4, decimal_places=2)
    measurment_unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "name",
            "brand",
        )


class Invoice(models.Model):
    products = models.ManyToManyField(Product, through="LineInInvoice")
    recipient = models.ForeignKey(
        Employee,
        on_delete=models.SET("Deleted"),
    )  # موظف الاستقبال
    supplier = models.ForeignKey(
        Compony,
        on_delete=models.SET("Deleted"),
    )
    received_date = models.DateField(auto_now_add=True)


class LineInInvoice(models.Model):  #  Many to Many RealtionShip Product + Invoice
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
    )
    packing = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        to_field="default_packing",
    )
    packing_price = models.DecimalField(max_digits=5, decimal_places=2)
    expire_date = models.DateField(blank=True, null=True)
    count_packing = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def total_price(self) -> float:
        return self.packing_price * self.count_packing

    class Meta:
        unique_together = [
            [
                "product",
                "invoice",
            ]
        ]


# TODO


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    required_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)
    comment = models.TextField(max_digits=200, decimal_places=2)
    products = models.ManyToManyField(Product, through="ProductOrder")

    # Invoice_Number	Charge or Cash Invoice Number	Int	11
    # OR_Number	Official Receipt Number	Int	11


class ProductOrder:
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    # TODO packing
    @property
    def packing(self):
        return self.product.packing

    @property
    def total_price(self) -> float:
        return self.quantity * self.price

    def __str__(self) -> str:
        return f"{self.product}-{self.order}"

    class Meta:
        unique_together = [
            [
                "product",
                "order",
            ]
        ]


class Deal(PolymorphicModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # Invoice_Number	Charge or Cash Invoice Number	Int	11
    down_payment = models.DecimalField(max_digits=5, decimal_places=2)  # دفعه قدمه
    rebate = models.DecimalField(max_digits=5, decimal_places=2)  # الخصم


class CashDeal(Deal):
    rebate_cash = models.DecimalField(max_digits=5, decimal_places=2)  #  خصم الكاش


class ChargeDeal(Deal):
    cost_charge = models.DecimalField(max_digits=5, decimal_places=2)  # تكلفه الشحن


class Supplier(Compony):
    brands = ArrayReferenceField(to=Brand, on_delete=models.CASCADE)
