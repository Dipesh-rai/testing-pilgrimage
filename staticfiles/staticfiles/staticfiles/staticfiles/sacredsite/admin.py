from django.contrib import admin
from django.utils.html import format_html
from .models import Sacredsite, Faq, Itinerary, Discounts,Gallery,Discount, TourBooking,Sacredpage

class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1
    fields = ('day_title', 'description')
    classes = ('collapse',)

class FaqInline(admin.TabularInline):
    model = Faq
    extra = 1
    fields = ('question', 'answer')
    classes = ('collapse',)

class DiscountsInline(admin.TabularInline):
    model = Discounts
    extra = 1
    fields = ('numberofpeople', 'price')
    classes = ('collapse',)

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    fileds = ('img','img_src')
    classes = ('collapse',)

class DiscountInline(admin.TabularInline):
    model = Discount
    extra = 1
    fields = ('min_participants', 'max_participants', 'discount_per_pax', 'discount_type')
    classes = ('collapse',)

@admin.register(Sacredsite)
class SacredsiteAdmin(admin.ModelAdmin):
    list_display = ('display_image', 'sacred_name', 'sacred_location', 'price_range', 'is_published')
    list_filter = ('is_published', 'Category')
    search_fields = ('sacred_name', 'sacred_location')
    inlines = [GalleryInline,ItineraryInline, FaqInline, DiscountsInline,DiscountInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('sacred_name', 'sacred_image','sacred_img_src', 'sacred_desc', 'sacred_location')
        }),
        ('Pricing & Duration', {
            'fields': ('sacred_price', 'sacred_days')
        }),
        ('Additional Details', {
            'fields': ('Destination', 'Total_Duration', 'Besttime', 'TripGrade', 
                      'Transportation', 'Accommodation', 'Style', 'Meals', 'MinGroupSize')
        }),
        ('Content', {
            'fields': ('overview', 'include', 'exclude', 'sitemap')
        }),
        ('Media', {
            'fields': ('banner_image', 'src_bannerimage')
        }),
        ('Status', {
            'fields': ('is_published', 'Category')  # Added Category here
        }),
    )
    
    # Remove prepopulated_fields since we're using AutoSlugField
    # Add sacred_slug to readonly_fields if you want to display it
    readonly_fields = ('sacred_slug',)

    def display_image(self, obj):
        if obj.sacred_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.sacred_image.url)
        return "No Image"
    display_image.short_description = 'Image'

    def price_range(self, obj):
        if obj.sacred_price:
            return f"${obj.sacred_price}"
        return "-"
    price_range.short_description = 'Price'

    def get_readonly_fields(self, request, obj=None):
        # Make slug read-only for existing objects
        if obj:  # editing an existing object
            return self.readonly_fields + ('sacred_slug',)
        return self.readonly_fields

    def display_image(self, obj):
        if obj.sacred_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.sacred_image.url)
        return "No Image"
    display_image.short_description = 'Image'

    def price_range(self, obj):
        if obj.sacred_price:
            return f"${obj.sacred_price}"
        return "-"
    price_range.short_description = 'Price'

    def discount_info(self, obj):
        discount = obj.discount.all()
        if not discount:
            return "No discounts"
        
        info = []
        for discount in discount:
            if discount.discount_type == 'percent':
                info.append(f"{discount.min_participants}+ pax: {discount.discount_per_pax}% off")
            else:
                info.append(f"{discount.min_participants}+ pax: ${discount.discount_per_pax} off")
        
        return ", ".join(info)
    discount_info.short_description = 'Discount Offers'

@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'package_link', 'email', 'booking_date', 'participants', 'status', 'created_at')
    list_filter = ('package', 'booking_date', 'status')
    search_fields = ('full_name', 'email', 'phone', 'package__sacred_name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'booking_date'
    list_select_related = ('package',)
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('package', 'full_name', 'email', 'phone')
        }),
        ('Trip Details', {
            'fields': ('booking_date', 'participants', 'special_requests')
        }),
        ('Status', {
            'fields': ('status', 'notes', 'created_at')
        }),
    )

    def package_link(self, obj):
        return format_html('<a href="{}">{}</a>', 
                         f'/admin/sacredsite/sacredsite/{obj.package.id}/change/',
                         obj.package.sacred_name)
    package_link.short_description = 'Package'
    package_link.admin_order_field = 'package__sacred_name'

@admin.register(Sacredpage)
class sacredpageAdmin(admin.ModelAdmin):
    list_display=('home_sacred_heading',)
    