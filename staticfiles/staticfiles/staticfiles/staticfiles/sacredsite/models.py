from django.db import models
from tinymce.models import HTMLField
from category.models import Category
from autoslug import AutoSlugField
from django.core.exceptions import ValidationError

# Create your models here.
class Sacredsite(models.Model):
    sacred_image=models.FileField(upload_to="sacredsite",max_length=250,null=True,default=None)
    sacred_img_src=models.CharField(max_length=100,blank="true",null="true")
    sacred_name=models.CharField(max_length=100)
    sacred_desc=HTMLField(blank=True,null=True)
    sacred_location=models.CharField(max_length=100)
    sacred_price=models.CharField(max_length=50)
    sacred_days=models.CharField(max_length=50,null=True,blank=True)
    banner_image=models.FileField(upload_to="banners",max_length=250,null=True,blank=True,default=None)
    src_bannerimage=models.CharField(null=True,blank=True)
    # 
    Destination=models.CharField(max_length=100,null=True,blank=True)
    Total_Duration=models.CharField(max_length=100,null=True,blank=True)
    Besttime=models.CharField(max_length=100,null=True,blank=True)
    TripGrade=models.CharField(max_length=100,null=True,blank=True)
    Transportation=models.CharField(max_length=100,null=True,blank=True)
    Accommodation=models.CharField(max_length=100,null=True,blank=True)
    Style=models.CharField(max_length=100,null=True,blank=True)
    Meals=models.CharField(max_length=100,null=True,blank=True)
    MinGroupSize=models.CharField(max_length=100,null=True,blank=True)
    courseduration=models.CharField(max_length=50,null=True,blank=True)
    # 
    overview=HTMLField()
    include=HTMLField(null=True,blank=True)
    exclude=HTMLField(null=True,blank=True)
    Category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sacredsite')
    sitemap=models.CharField(null=True,blank=True)
    sacred_slug=AutoSlugField(populate_from='sacred_name',unique=True,null=True,default=None)
    is_published = models.BooleanField(default=True)
    def get_related_sites(self, limit=4):
        """
        Returns related sacred sites from the same category, excluding current site
        """
        return Sacredsite.objects.filter(
            Category=self.Category,
            is_published=True
        ).exclude(
            id=self.id
        ).order_by('?')[:limit]  # Random order
    
    def __str__(self):
        return self.sacred_name


class Itinerary(models.Model):
    sacredsite = models.ForeignKey(Sacredsite, on_delete=models.CASCADE, related_name='itineraries')
    day_title = models.CharField(max_length=255,blank=True,null=True)
    description = HTMLField(blank=True,null=True)

    def __str__(self):
        return f"Itinerary: {self.day_title}"
    
   

class Faq(models.Model):
    sacredsite = models.ForeignKey(Sacredsite, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255,blank=True,null=True)
    answer = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"FAQ: {self.question[:30]}..."
    
class Discounts(models.Model):
    sacredsite = models.ForeignKey('sacredsite.Sacredsite', on_delete=models.CASCADE, related_name='discounts')
    numberofpeople = models.CharField(max_length=255,blank=True,null=True)
    price = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Discounts: {self.numberofpeople}"
    
class Discount(models.Model):
    sacredsite = models.ForeignKey(Sacredsite, on_delete=models.CASCADE, related_name='discount')
    min_participants = models.PositiveIntegerField(
        help_text="Minimum number of participants for this discount"
    )
    max_participants = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Maximum number of participants for this discount (leave blank for no limit)"
    )
    discount_per_pax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Discount amount per participant"
    )
    discount_type = models.CharField(
        max_length=10,
        choices=[('percent', 'Percentage'), ('fixed', 'Fixed Amount')],
        default='fixed',
        help_text="Type of discount to apply"
    )

    def __str__(self):
        if self.discount_type == 'percent':
            return f"{self.discount_per_pax}% off per pax ({self.min_participants}+ people)"
        return f"${self.discount_per_pax} off per pax ({self.min_participants}+ people)"
    
class Gallery(models.Model):
    sacredsite = models.ForeignKey('sacredsite.Sacredsite', on_delete=models.CASCADE, related_name='gallery')
    img=models.FileField(upload_to="sacredsite",max_length=250,null=True,default=None)
    img_src=models.TextField(blank=True,null=True)

    def __str__(self):
        return f"Gallery:{self.id}"

    def get_related_tours(self,limit=3):
        return Tour.object.filter(category=self.category).exclude(id=self.id).order_by('?')[:limit]

class Sacredpage(models.Model):
    home_sacred_heading=models.CharField(max_length=100,blank="true",null="true")
    home_sacred_shortdescription=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.home_sacred_heading

class TourBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    package = models.ForeignKey(Sacredsite, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    booking_date = models.DateField()
    participants = models.PositiveIntegerField(default=1)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.package.sacred_name}"

    def calculate_discounted_price(self):
        base_price = Decimal(self.package.sacred_price)
        total_discount = Decimal(0)
        
        # Find applicable discounts
        discount = self.package.discounts.filter(
            min_participants__lte=self.participants
        ).order_by('-min_participants')
        
        if discount.exists():
            best_discount = discount.first()
            if best_discount.discount_type == 'percent':
                discount_per_pax = base_price * (best_discount.discount_per_pax / 100)
            else:
                discount_per_pax = best_discount.discount_per_pax
            
            total_discount = discount_per_pax * self.participants
        
        return base_price - total_discount

    def get_final_price(self):
        return self.calculate_discounted_price()