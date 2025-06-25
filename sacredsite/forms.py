from django import forms
from .models import TourBooking

class TourBookingForm(forms.ModelForm):
    class Meta:
        model = TourBooking
        fields = ['package', 'full_name', 'email', 'phone', 'booking_date', 'participants', 'special_requests']
        widgets = {
            'package': forms.HiddenInput(),
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }