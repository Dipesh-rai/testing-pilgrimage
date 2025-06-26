from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class Contact(models.Model):
    banner_image=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    contact_des=models.CharField(max_length=100,blank=True,null=True)
    second_heading=models.CharField(max_length=100,blank=True,null=True)
    short_description=models.CharField(max_length=100,blank=True,null=True)
    call_us_name=models.CharField(max_length=100,blank=True,null=True)
    telphone_number_1=models.CharField(max_length=100,blank=True,null=True)
    telephone_number_2=models.CharField(max_length=100,blank=True,null=True)
    whatsapp_number=models.CharField(max_length=100,blank=True,null=True)
    Email_us_name=models.CharField(max_length=100,blank=True,null=True)
    email=models.CharField(max_length=100,blank=True,null=True)
    email_2=models.CharField(max_length=100,blank=True,null=True)
    Visit_us_name=models.CharField(max_length=100,blank=True,null=True)
    location_address_name=models.CharField(max_length=100,blank=True,null=True)
    location_street=models.CharField(blank=True,null=True)
    location_city=models.CharField(blank=True,null=True)
    country=models.CharField(blank=True,null=True)
    office_opendays=models.CharField(max_length=100,blank=True,null=True)
    office_time=models.CharField(max_length=100,blank=True,null=True)
    short_heading_office=models.CharField(max_length=100,blank=True,null=True)
    short_description=models.CharField(max_length=100,blank=True,null=True)
    FAQ=HTMLField(blank=True,null=True)

