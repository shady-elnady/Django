from django.db import models

# Create your models here.

class Language(models.Model):
  name = models.CharField(max_length=50, unique=True)
  code = models.CharField(max_length=5, unique=True)
  rtl = models.BooleanField(default=False)
  
  def __str__(self) -> str:
    return self.name