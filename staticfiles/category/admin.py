from django.contrib import admin
from category.models import Category, Category_page

# Register your models here.
class categoryAdmin(admin.ModelAdmin):
    list_display=('category_name','icon_name')
    
admin.site.register(Category,categoryAdmin)

class categorypageAdmin(admin.ModelAdmin):
    list_display=('category_banner_img','Main_heading','short_description','name','description')
    
admin.site.register(Category_page,categorypageAdmin)
