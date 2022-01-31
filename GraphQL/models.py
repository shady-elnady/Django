from django.db import models

# Create your models here.
    

class BaseModel(models.Model):
  create_date = models.DateTimeField(auto_now_add=True, editable=False)
  last_updated = models.DateTimeField(auto_now=True, editable=False)

  class Meta:
    abstract = True
      
      
class BaseModelName(models.Model):
  name = models.CharField(max_length=50, primary_key=True)
  
  def __str__(self) -> str:
    return self.name
    
  class Meta:
    abstract = True
      

class BaseModelNative(BaseModelName):
  native = models.CharField(max_length=20, unique=True, null=True, blank=True)
  
  class Meta:
    abstract = True
    
    
class BaseModelEmoji(BaseModelName):
  emoji = models.CharField(max_length=5, unique=True, null=True, blank=True)
  
  class Meta:
    abstract = True
    
    
class BaseModelLogo(BaseModelName):
  logo_url = models.CharField(max_length=100, unique=True, null=True, blank=True)
  
  class Meta:
    abstract = True
    
