from django.contrib import admin
from .models import Home,Commitment,Short_description
# Register your models here.

class commitAdmin(admin.ModelAdmin):
    list_display=('commitment_heading','commitment_description','commitment_img')
admin.site.register(Commitment,commitAdmin)

class homeAdmin(admin.ModelAdmin):
    list_display=('banner_img','h1_Name','short_description')
admin.site.register(Home,homeAdmin)

class shortdescriptionAdmin(admin.ModelAdmin):
    list_display=('image','description')
admin.site.register(Short_description,shortdescriptionAdmin)