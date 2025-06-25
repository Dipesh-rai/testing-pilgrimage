from django.db import models
from tinymce.models import HTMLField
from tinymce.models import HTMLField
# Create your models here.
class Home(models.Model):
    banner_img=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    h1_Name=models.CharField(max_length=100,blank=True,null=True)
    short_description=models.CharField(max_length=100,blank=True,null=True)
   
class Commitment(models.Model):
    commitment_heading=models.CharField(max_length=100,blank=True,null=True)
    commitment_description=HTMLField(blank=True,null=True)
    commitment_img=models.FileField(upload_to="sacredsite",max_length=250,null=True,default=None)

class Short_description(models.Model):
    image=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    description=HTMLField(blank=True,null=True)