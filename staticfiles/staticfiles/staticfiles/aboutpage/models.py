from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class About(models.Model):
    banner_img=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    img_alt_name=models.CharField(max_length=100,blank=True,null=True)
    banner_heading=models.CharField(max_length=100,blank=True,null=True)
    banner_short_description=HTMLField(blank=True,null=True)
    description=HTMLField(blank=True,null=True)


class Ourmission(models.Model):
    banner_img=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    img_alt_name=models.CharField(max_length=100,blank=True,null=True)
    banner_heading=models.CharField(max_length=100,blank=True,null=True)
    banner_short_description=HTMLField(blank=True,null=True)
    description=HTMLField(blank=True,null=True)

class Whytravel(models.Model):
    banner_img=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    img_alt_name=models.CharField(max_length=100,blank=True,null=True)
    banner_heading=models.CharField(max_length=100,blank=True,null=True)
    banner_short_description=HTMLField(blank=True,null=True)
    description=HTMLField(blank=True,null=True)
