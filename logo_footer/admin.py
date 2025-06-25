from django.contrib import admin
from .models import Logo, Footer
# Register your models here.
class LogoAdmin(admin.ModelAdmin):
    list_display=('logo_img','logo_name')
admin.site.register(Logo,LogoAdmin)

class FooterAdmin(admin.ModelAdmin):
    list_display=('description',)
admin.site.register(Footer,FooterAdmin)