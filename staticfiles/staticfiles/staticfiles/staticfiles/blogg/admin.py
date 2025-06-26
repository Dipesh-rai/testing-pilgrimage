from django.contrib import admin
from .models import Blogpages, Blog
# Register your models here.

class BlogpageAdmin(admin.ModelAdmin):
    list_display = ('banner_image', 'main_heading', 'short_description', 'second_heading', 'description')
admin.site.register(Blogpages, BlogpageAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('display_blog_img','blog_title', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')  # Add filters for dates
    search_fields = ('blog_title', 'blog_description')  # Add search functionality
    readonly_fields = ('created_at', 'updated_at')  # Make date fields read-only
    date_hierarchy = 'created_at'  # Add date hierarchy navigation
    
    # Custom method to display truncated description
    def truncated_description(self, obj):
        return obj.blog_description[:100] + '...' if len(obj.blog_description) > 100 else obj.blog_description
    truncated_description.short_description = 'Description Preview'
    
    def display_blog_img(self, obj):
        if obj.blog_img:  # Check if blog_img exists
            from django.utils.html import format_html  # Import format_html here or at top
            return format_html('<img src="{}" width="50" height="50" />', obj.blog_img.url)
        return "No Image"
    display_blog_img.short_description = 'Image'
    
admin.site.register(Blog, BlogAdmin)