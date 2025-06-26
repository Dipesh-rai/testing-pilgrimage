from django.contrib import admin
from .models import About,Ourmission,Whytravel
# Register your models here.
class aboutAdmin(admin.ModelAdmin):
    list_display=('banner_img','description')
admin.site.register(About,aboutAdmin)

class ourmissionadmin(admin.ModelAdmin):
    list_display=('banner_img','img_alt_name','description')
admin.site.register(Ourmission,ourmissionadmin)

class whytravelAdmin(admin.ModelAdmin):
    list_display=('banner_img','img_alt_name','description')
admin.site.register(Whytravel,whytravelAdmin)