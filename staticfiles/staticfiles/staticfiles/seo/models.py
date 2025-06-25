from django.db import models

# Create your models here.
# seo/models.py
class SEO(models.Model):
    page_slug = models.CharField(max_length=100, unique=True)  # like 'home', 'about', 'services/sacred-trek'
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=160)
    canonical = models.URLField(blank=True, null=True)
    og_title = models.CharField(max_length=70)
    og_description = models.CharField(max_length=300)
    og_image = models.URLField(blank=True, null=True)
    og_type = models.CharField(max_length=20, default='website')

    def __str__(self):
        return self.page_slug

