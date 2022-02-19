from django.db import models
from django.forms import CharField
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

# from django.utils.text import slugify
from djongo.models import ArrayField
from timezone_field import TimeZoneField
from Facilities.models import MobileNetWork
from GraphQL.models import BaseModelLogo, BaseModelNative
from Payment.models import Currency
from Languages.models import Language


# Create your models here.


class Continent(models.Model):
    class Continents(models.TextChoices):
        AF = _("Africa")
        AS = _("Asia")
        EU = _("Europe")
        NA = _("North America")
        OC = _("Oceania")
        SA = _("South America")
        AN = _("Antarctica")

    name = models.CharField(
        max_length=2,
        primary_key=True,
        choices=Continents.choices,
        verbose_name=_("Continent Name"),
    )

    class Meta:
        abstract = True
        verbose_name = _("Continent")
        verbose_name_plural = _("Continents")


class Country(BaseModelNative):

    continents = ArrayField(
        model_container=Continent,
        verbose_name=_("Continents"),
    )
    capital = models.CharField(
        max_length=20,
        verbose_name=_("Capital"),
    )
    flag = models.CharField(
        max_length=5,
        verbose_name=_("Flag Emoji"),
    )
    flags_svg = models.ImageField(
        upload_to="svg/flags/",
        blank=True,
        null=True,
        verbose_name=_("Flags SVG"),
    )
    postalCode = models.CharField(
        max_length=5,
        verbose_name=_("Postal Code"),
    )
    timezones = TimeZoneField(
        default="Africa/Cairo",
        verbose_name=_("Time Zone"),
    )
    currencies = ArrayField(
        model_container=Currency,
        verbose_name=_("Currencies"),
    )
    languages = ArrayField(
        model_container=Language,
        verbose_name=_("Currencies"),
    )
    Tel_code = models.CharField(
        max_length=3,
        verbose_name=_("Telphone Code"),
    )

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})


class Province(BaseModelNative):  # المحافظه
    tel_code = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Telphone Code"),
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name=_("Country"),
    )

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")


class City(BaseModelNative):
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name=_("Province"),
    )

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")


class Village(BaseModelNative):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name=_("City"),
    )

    class Meta:
        verbose_name = _("Village")
        verbose_name_plural = _("Villages")


class Street(BaseModelNative):
    village = models.ForeignKey(
        Village,
        on_delete=models.CASCADE,
        verbose_name=_("Village"),
    )

    class Meta:
        verbose_name = _("Street")
        verbose_name_plural = _("Streets")


class WayCommunicate(PolymorphicModel):
    owner = models.ForeignKey(
        "Persons.Person",
        on_delete=models.CASCADE,
        verbose_name=_("Owner"),
        related_name="%(app_label)s_%(class)s_Owner",
    )

    class Meta:
        verbose_name = _("Way Communicate")
        verbose_name_plural = _("Way Communicates")


class Address(BaseModelNative, WayCommunicate):
    street = models.ForeignKey(
        Street,
        on_delete=models.CASCADE,
        verbose_name=_("Street"),
    )
    house = models.CharField(
        max_length=50,
        verbose_name=_("House"),
    )
    # TODO Location Google Maps
    location = models.CharField(
        max_length=100,
        verbose_name=_("Location"),
    )  # add Lat and Lang for Google Maps

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Address")


class Phone(WayCommunicate):
    country_code = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name=_("Country Code"),
        related_name="%(app_label)s_%(class)s_Country_Code",
    )
    rest_number = models.CharField(max_length=7, verbose_name=_("Phone Number"))

    class Meta:
        verbose_name = _("Phone")
        verbose_name_plural = _("Phones")


class Mobile(Phone):
    mobile_netWork_code = models.ForeignKey(
        MobileNetWork,
        to_field="tel_code",
        on_delete=models.CASCADE,
        verbose_name=_("Mobile NetWork Code"),
        related_name="%(app_label)s_%(class)s_Mobile_NetWork_Code",
    )

    @property
    def number(self):
        return f"{str(self.country_code)}{str(self.mobile_netWork_code)}{str(self.rest_number)}"

    class Meta:
        verbose_name = _("Mobile")
        verbose_name_plural = _("Mobiles")


class LandPhone(Phone):
    province_code = models.ForeignKey(
        Province,
        to_field="tel_code",
        on_delete=models.CASCADE,
        verbose_name=_("Province Code"),
        related_name="%(app_label)s_%(class)s_Province_Code",
    )

    @property
    def number(self):
        return (
            f"{str(self.country_code)}{str(self.province_code)}{str(self.rest_number)}"
        )

    class Meta:
        verbose_name = _("Land Phone")
        verbose_name_plural = _("Land Phones")


class SocialMedia(BaseModelLogo, WayCommunicate):
    mobile = models.ForeignKey(
        Mobile,
        on_delete=models.CASCADE,
        verbose_name=_("Mobile"),
        related_name="%(app_label)s_%(class)s_Mobile",
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Social Media")
        verbose_name_plural = _("Social Medias")


class EMail(SocialMedia):
    @property
    def email(self):
        return f"{self.name}@{self.__class__.__name__}.com".lower()

    class Meta:
        verbose_name = _("EMail")
        verbose_name_plural = _("EMails")


class GMail(EMail):
    class Meta:
        verbose_name = _("GMail")
        verbose_name_plural = _("GMails")


class Apple(EMail):
    class Meta:
        verbose_name = _("Apple")
        verbose_name_plural = _("Apples")


class GitHub(EMail):
    class Meta:
        verbose_name = _("GitHub")
        verbose_name_plural = _("GitHubs")


class Yahoo(EMail):
    class Meta:
        verbose_name = _("Yahoo")
        verbose_name_plural = _("Yahoos")


class Microsoft(EMail):
    class Meta:
        verbose_name = _("Microsoft")
        verbose_name_plural = _("Microsofts")


class SkyBye(EMail):
    class Meta:
        verbose_name = _("SkyBye")
        verbose_name_plural = _("SkyByes")


class WhatsApp(SocialMedia):
    class Meta:
        verbose_name = _("WhatsApp")
        verbose_name_plural = _("WhatsApps")


class Telegrame(SocialMedia):
    class Meta:
        verbose_name = _("Telegrame")
        verbose_name_plural = _("Telegrames")


class Instagram(SocialMedia):
    class Meta:
        verbose_name = _("Instagram")
        verbose_name_plural = _("Instagrams")


class Imo(SocialMedia):
    class Meta:
        verbose_name = _("Imo")
        verbose_name_plural = _("Imos")


class SocialMediaE(SocialMedia):
    e_mail = models.ForeignKey(
        EMail,
        on_delete=models.CASCADE,
        verbose_name=_("EMail"),
        related_name="%(app_label)s_%(class)s_EMail",
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("SocialMediaE")
        verbose_name_plural = _("SocialMediaEs")


class FaceBook(SocialMediaE):
    class Meta:
        verbose_name = _("FaceBook")
        verbose_name_plural = _("FaceBooks")


class Twitter(SocialMediaE):
    class Meta:
        verbose_name = _("Twitter")
        verbose_name_plural = _("Twitters")


class Linkedin(SocialMediaE):
    class Meta:
        verbose_name = _("Linkedin")
        verbose_name_plural = _("Linkedins")


##
class Caller(models.Model):
    way_communicate = models.ManyToManyField(
        WayCommunicate,
        verbose_name=_("Way Communicate"),
        related_name="%(app_label)s_%(class)s_Way_Communicate",
    )

    class Meta:
        verbose_name = _("Caller")
        verbose_name_plural = _("Callers")


# TODO API FOR COUNTRIES
# https://restcountries.com/#api-endpoints-v3
""" 
    {
        "name": {
            "common": "Egypt",
            "official": "Arab Republic of Egypt",
            "nativeName": {
                "ara": {
                    "official": "جمهورية مصر العربية",
                    "common": "مصر"
                }
            }
        },
        "tld": [
            ".eg",
            ".مصر"
        ],
        "cca2": "EG",
        "ccn3": "818",
        "cca3": "EGY",
        "cioc": "EGY",
        "independent": true,
        "status": "officially-assigned",
        "unMember": true,
        "currencies": {
            "EGP": {
                "name": "Egyptian pound",
                "symbol": "£"
            }
        },
        "idd": {
            "root": "+2",
            "suffixes": [
                "0"
            ]
        },
        "capital": [
            "Cairo"
        ],
        "altSpellings": [
            "EG",
            "Arab Republic of Egypt"
        ],
        "region": "Africa",
        "subregion": "Northern Africa",
        "languages": {
            "ara": "Arabic"
        },
        "translations": {
            "ara": {
                "official": "جمهورية مصر العربية",
                "common": "مصر"
            },
            "ces": {
                "official": "Egyptská arabská republika",
                "common": "Egypt"
            },
            "cym": {
                "official": "Gweriniaeth Arabaidd yr Aifft",
                "common": "Yr Aifft"
            },
            "deu": {
                "official": "Arabische Republik Ägypten",
                "common": "Ägypten"
            },
            "est": {
                "official": "Egiptuse Araabia Vabariik",
                "common": "Egiptus"
            },
            "fin": {
                "official": "Egyptin arabitasavalta",
                "common": "Egypti"
            },
            "fra": {
                "official": "République arabe d'Égypte",
                "common": "Égypte"
            },
            "hrv": {
                "official": "Arapska Republika Egipat",
                "common": "Egipat"
            },
            "hun": {
                "official": "Egyiptomi Arab Köztársaság",
                "common": "Egyiptom"
            },
            "ita": {
                "official": "Repubblica araba d'Egitto",
                "common": "Egitto"
            },
            "jpn": {
                "official": "エジプト·アラブ共和国",
                "common": "エジプト"
            },
            "kor": {
                "official": "이집트 아랍 공화국",
                "common": "이집트"
            },
            "nld": {
                "official": "Arabische Republiek Egypte",
                "common": "Egypte"
            },
            "per": {
                "official": "جمهوری عربی مصر",
                "common": "مصر"
            },
            "pol": {
                "official": "Arabska Republika Egiptu",
                "common": "Egipt"
            },
            "por": {
                "official": "República Árabe do Egipto",
                "common": "Egito"
            },
            "rus": {
                "official": "Арабская Республика Египет",
                "common": "Египет"
            },
            "slk": {
                "official": "Egyptská arabská republika",
                "common": "Egypt"
            },
            "spa": {
                "official": "República Árabe de Egipto",
                "common": "Egipto"
            },
            "swe": {
                "official": "Arabrepubliken Egypten",
                "common": "Egypten"
            },
            "urd": {
                "official": "مصری عرب جمہوریہ",
                "common": "مصر"
            },
            "zho": {
                "official": "阿拉伯埃及共和国",
                "common": "埃及"
            }
        },
        "latlng": [
            27,
            30
        ],
        "landlocked": false,
        "borders": [
            "ISR",
            "LBY",
            "PSE",
            "SDN"
        ],
        "area": 1002450,
        "demonyms": {
            "eng": {
                "f": "Egyptian",
                "m": "Egyptian"
            },
            "fra": {
                "f": "Égyptienne",
                "m": "Égyptien"
            }
        },
        "flag": "🇪🇬",
        "maps": {
            "googleMaps": "https://goo.gl/maps/uoDRhXbsqjG6L7VG7",
            "openStreetMaps": "https://www.openstreetmap.org/relation/1473947"
        },
        "population": 102334403,
        "gini": {
            "2017": 31.5
        },
        "fifa": "EGY",
        "car": {
            "signs": [
                "ET"
            ],
            "side": "right"
        },
        "timezones": [
            "UTC+02:00"
        ],
        "continents": [
            "Africa"
        ],
        "flags": {
            "png": "https://flagcdn.com/w320/eg.png",
            "svg": "https://flagcdn.com/eg.svg"
        },
        "coatOfArms": {
            "png": "https://mainfacts.com/media/images/coats_of_arms/eg.png",
            "svg": "https://mainfacts.com/media/images/coats_of_arms/eg.svg"
        },
        "startOfWeek": "sunday",
        "capitalInfo": {
            "latlng": [
                30.05,
                31.25
            ]
        },
        "postalCode": {
            "format": "#####",
            "regex": "^(\\d{5})$"
        }
    }
"""
