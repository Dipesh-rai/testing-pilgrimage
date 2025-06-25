from django.contrib import admin
from .models import Contact
# Register your models here.
class contactAdmin(admin.ModelAdmin):
    list_display=('banner_image','contact_des','second_heading','short_description','call_us_name','telphone_number_1','telephone_number_2','Email_us_name','email','email_2','Visit_us_name','location_address_name','office_opendays','office_time','short_heading_office','short_description','FAQ')
admin.site.register(Contact,contactAdmin)