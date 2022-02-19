from django.db import models
from GraphQL.models import BaseModelNative
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

# Create your models here.


class Currency(BaseModelNative):
    code = models.CharField(
        max_length=3,
        unique=True,
        verbose_name=_("Code"),
    )
    emoji = models.CharField(
        max_length=3,
        unique=True,
        verbose_name=_("Emoji"),
    )
    equal_dolar = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        verbose_name=_("Equal Dolar"),
        blank=True,
        null=True,
    )
    last_update = models.DateField(
        auto_now=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")


def currencyExchange():
    pass

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

    # TODO PAYMENT
    # class Payment:
    #     class PayMethod(models.TextChoices):
    #         check = "Check"
    #         PayPal = "PayPal"

    #     payment_method = models.CharField(max_length=10, choices=PayMethod.choices)
    #     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    #     payment_date = models.DateTimeField(auto_now_add=True)
    #     amount = models.DecimalField(max_digits=5, decimal_places=2)  #  المبلغ
    #     currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    # TODO CURRENCY API
    # https://m3o.com/account/keys

    # API_key =  N2Q1OWUwNDctZDM4Ny00MDNkLWIxOGUtYWM1MTJlNGExYTUx

    """
        curl "https://api.m3o.com/v1/currency/Codes" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $M3O_API_TOKEN" \
        -d '{}'
    """


##  https://openexchangerates.org/account/app-ids
# api ID = 82775e187c684ecaa9efc98e7f0e9381
