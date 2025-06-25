from django import forms
from .models import Subscriber
# Create your models here.
class SubsciptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Enter Your email'
            })
        }

