from django.db import models
from GraphQL.models import BaseModelNative
from Persons.models import Customer

# Create your models here.


class Currency(BaseModelNative):
    code = models.CharField(max_length=5, blank=True, null=True, unique=True)
    emoji = models.CharField(max_length=5, blank=True, null=True, unique=True)


# TODO Paymant
class Payment:
    class PayMethod(models.TextChoices):
        check = "Check"
        PayPal = "PayPal"

    payment_method = models.CharField(max_length=10, choices=PayMethod.choices)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)  #  المبلغ
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
