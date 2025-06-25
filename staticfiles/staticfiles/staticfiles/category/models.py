from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField

# Create your models here.
class Category(models.Model):
    category_name=models.CharField( max_length=100 )
    sacred_slug=AutoSlugField(populate_from='category_name',unique=True,null=True,default=None)
    icon_name=models.CharField( max_length=100,null=True,default=None,blank=True)
    category_banner_img=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    Main_heading=models.CharField(max_length=100,null=True,blank=True)
    short_description=HTMLField(null=True,blank=True)
    About=models.CharField(max_length=100,null=True,blank=True)
    description=HTMLField(null=True,blank=True)
    category_img= models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
   

    def __str__(self):
        return self.category_name
    
class Category_page(models.Model):
    category_banner_img=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    Main_heading=models.CharField(max_length=100,null=True,blank=True)
    short_description=HTMLField(null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    description=HTMLField(null=True,blank=True)
    home_category_title=models.CharField(max_length=100,null=True,blank=True)
    home_category_shortdecription=HTMLField(null=True,blank=True)
    def __str__(self):
        return self.name