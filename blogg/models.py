from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
# Create your models here.
class Blogpages(models.Model):
    banner_image=models.FileField(upload_to="sacredsite",max_length=250,null=True,default=None)
    banner_img_src=models.CharField(max_length=100,null=True,blank=True)
    main_heading=models.CharField(max_length=100,null=True,blank=True)
    short_description=HTMLField(null=True,blank=True)
    second_heading=models.CharField(max_length=100,null=True,blank=True)
    description=HTMLField(null=True,blank=True)
    home_blog_title=models.CharField(max_length=100,null=True,blank=True)
    home_blog_description=HTMLField(null=True,blank=True)

class Blog(models.Model):
    blog_img=models.FileField(upload_to="sacredsite",max_length=250,null=True,default=None)
    img_src=models.CharField(max_length=200,blank=True,null=True)
    banner_img=models.FileField(upload_to="sacredsite",max_length=250,null=True,default=None)
    banner_img_src=models.CharField(max_length=100,null=True,blank=True)
    blog_title=models.CharField(max_length=200)
    blog_description=HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      
    blog_slug = AutoSlugField(populate_from='blog_title',unique=True,null=True,default=None)
    def get_related_blog(self,limit=4):
        """
        Returns related blog 
        """
        return Blog.objects.filter(

        ).exclude(
            id=self.id
        ).order_by('?')[:limit]
    def __str__(self):
        return self.blog_title