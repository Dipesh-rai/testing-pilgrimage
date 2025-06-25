"""
URL configuration for pilgrimage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from pilgrimage import views
from .views import check_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage,name="homepage"),
    path('category/sacredsite', views.sacredsite,name="sacredsite"),
    path('category/sacredsite/<slug:slug>/', views.journeyDetails,name="journeyDetails"),
    path('category', views.categorypages,name="categorypages"),
    path('blog', views.blog,name="blog"),
    path('blog/<slug>', views.blogpages,name="blogpages"),
    path('contact', views.contact,name="contact"),
    path('saveenquiry', views.saveenquiry,name="saveenquiry"),
    path('about', views.about,name="about"),
    path('activities', views.activities,name="activities"),
    path('ourmission', views.ourmission,name="ourmission"),
    path('whytravelwithus', views.whytravel, name="whytravel"),
    path('newsdetails/<slug>', views.newsDetails,name="newsdetails"),
    path('check-email/', check_email, name='check_email'),
    # path('book/<slug:slug>/', book_tour, name='book_tour'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
