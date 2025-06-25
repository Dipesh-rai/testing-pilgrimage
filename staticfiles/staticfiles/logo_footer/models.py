from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class Logo(models.Model):
    logo_img=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    logo_name=models.CharField(max_length=30,blank=True,null=True)
    # fav_icon=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    def __str__(self):
        return self.logo_name

class Footer(models.Model):
    description=HTMLField(blank=True,null=True)
    def __str__(self):
        return self.description[:50]