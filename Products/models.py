from django.db import models
from GraphQL.models import BaseModel, BaseModelName
from polymorphic.models import PolymorphicModel
from Persons.models import TeamEmployee

# Create your models here.


class Brand(BaseModelName):
    # made_in = models.ForeignKey(
    #     Country, related_name='brands', on_delete=models.CASCADE,
    # )
    logo_url = models.CharField(max_length=100, null=True, blank=True)


class Compony(BaseModelName, BaseModel):
    logo_url = models.CharField(max_length=100, null=True, blank=True)


class MainCategory(BaseModelName):
    pass


class Stored(BaseModelName, BaseModel):
    pass


class SubCategory(BaseModelName):
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)


class Product(PolymorphicModel, BaseModelName, BaseModel):  # Weak Entity
    brand = models.ForeignKey(
        Brand, related_name="products", on_delete=models.CASCADE,
    )
    serial = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    volume = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta:
        unique_together = (
            'name',
            'brand',
        )


class Invoice(models.Model):
    products = models.ManyToManyField(Product, through='LineInInvoice')
    recipient = models.ForeignKey(
        TeamEmployee, related_name='recipient_invoice', on_delete=models.SET('Deleted'),
    )
    company = models.ForeignKey(
        Compony, related_name='sender_company', on_delete=models.SET('Deleted'),
    )
    _date = models.DateField()


class LineInInvoice(models.Model):  # NOTE Man to Many RealtionShip Product + Invoice
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
    )
    unit_price = models.DecimalField(max_digits=4, decimal_places=2)
    expire_date = models.DateField()
    Quantity = models.PositiveSmallIntegerField()
    total_price = models.DecimalField(
        max_digits=4, decimal_places=2,
    )  # TODO Calculated Field

    class Meta:
        unique_together = [
            [
                'invoice',
                'product',
            ]
        ]
