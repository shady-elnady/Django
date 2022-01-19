from django.db import models
from GraphQL.models import BaseModel, BaseModelName, BaseModelNative
from djongo.models import ArrayField
from Products.models import Product

# Create your models here.



class Sample(BaseModelName):
  Comment = models.TextField(max_length=200)


class AntiBiotic(BaseModelName):
  code = models.CharField(max_length=10, unique=True)
  for_child_pregnant = models.BooleanField(default=True)


class Unit(BaseModelName):
  pass

class ShortCutParameter(models.Model):
  name = models.CharField(max_length=30)

  class Meta:
    abstract = True

class Parameter(BaseModelName):
  shortcuts = ArrayField(
    model_container=ShortCutParameter,
  )
  units = models.ManyToManyField(Unit)


class BloodGroup(BaseModelName):   # ENUM
  class ABOSystem(models.TextChoices):
    A = 'A'
    B = 'B'
    AB = 'AB'
    O = 'O'
  class Rh_Type(models.TextChoices):
    Positive = 'Positive'
    Negative = 'Negative' 
  ABO_system = models.CharField(max_length=2, choices=ABOSystem.choices)
  Rh_type = models.CharField(max_length=10, choices=Rh_Type.choices)
  class Meta:
    unique_together = (
      "ABO_system",
      "Rh_type",
    )


class Senstivity(models.Model):   # ENUM
  class Senstive(models.TextChoices):
    Strong = 'Strong'
    Mmderate = 'Moderate'
    weak = 'Weak'
    very_weak = 'Very Weak'
  name = models.CharField(max_length=10, primary_key=True, choices=Senstive.choices)
  
  
class HighLow(models.Model):   # ENUM
  class HL(models.TextChoices):
    high = 'High'
    low = 'Low'
  name = models.CharField(max_length=10, primary_key=True, choices=HL.choices)


class Departement(BaseModelName):
  pass

class Technique(BaseModelName):
  pass


class Analyzer(BaseModelName, BaseModel):
  serial = models.CharField(max_length=50, unique=True)
  brochu_url = models.CharField(max_length=50, null=True, blank=True)
  test_volume = models.SmallIntegerField()


class Kat(BaseModel):
  serial = models.OneToOneField(
      Product, on_delete=models.CASCADE, related_name="kats",
  )
    

# class Telephone(BaseModelNative):
#     pass


#  🧕   🕌   🕋  👳  💲  🌍  👰‍♂️   👰‍♀️   👩‍❤️‍💋‍👩   🤰🏻   🏋️‍♀️   💒   👩‍❤️‍💋‍👨   🧑🏼‍🍼  👩‍🎓   🚣‍♀️  🤾‍♀️  👨‍💼   👷🏽‍♂️  👷🏼‍♀️   👨‍🔧   👨‍⚕  👩🏽‍⚕️  👨🏻‍🎓  👨🏼‍🏫  👩🏽‍🏫   🦷
