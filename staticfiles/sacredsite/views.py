from django.shortcuts import render
from .models import Sacredsite
from django.views.generic import DetailView
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
import json

class JourneyDetailView(DetailView):
    model = Sacredsite
    template_name = 'viewjourney.html'
    context_object_name = 'journeyDetails'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        journeyDetails = self.get_object()
        context['journeyDetails_json']=json.dumps({
            'sacred_days':journeyDetails.sacred_days
        })
        return context
# Create your views here.
