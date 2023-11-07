"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from home.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index ,name = 'home'),
    path('listings/', listings , name='listings'),
    path('dashboard/', dashboard , name='dashboard'),
    path('property-single/<int:listing_id>', property_single, name='property_single'),
    path('contact/',contact, name='contact'),
    path('services/',services, name='services'),
    path('contactus/',contactus, name='contactus'),
    path('realtor/',realtors, name='realtors'),
    path('about/', about ,name ='about'),
    path('login/', login, name='login'),
    path('logout', logout, name='logout'),
    path('register/', register, name='register'),
    path('realtorregistration/', realtorregistration, name='realtorregistration'),
    path('search_listings/', search_listings, name='search_listings'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

