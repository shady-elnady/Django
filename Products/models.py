from django.db import models
from Facilities.models import Compony
from GraphQL.models import BaseModel, BaseModelName
from polymorphic.models import PolymorphicModel
from Persons.models import TeamEmployee

# Create your models here.


class Brand(BaseModelName):
    # made_in = models.ForeignKey(
    #     Country, related_name='brands', on_delete=models.CASCADE,
    # )
    logo_url = models.CharField(max_length=100, null=True, blank=True)


class MainCategory(BaseModelName):
    pass


class SubCategory(BaseModelName):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)


class Product(PolymorphicModel, BaseModelName, BaseModel):  # Weak Entity
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
    )
    serial = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    volume = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = (
            "name",
            "brand",
        )


class Invoice(models.Model):
    products = models.ManyToManyField(Product, through="LineInInvoice")
    recipient = models.ForeignKey(
        TeamEmployee,
        on_delete=models.SET("Deleted"),
    )
    company = models.ForeignKey(
        Compony,
        on_delete=models.SET("Deleted"),
    )
    _date = models.DateField()


class LineInInvoice(models.Model):  #  Many to Many RealtionShip Product + Invoice
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
    )
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    expire_date = models.DateField()
    quantity = models.DecimalField(max_digits=5, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    class Meta:
        unique_together = [
            [
                "product",
                "invoice",
            ]
        ]
