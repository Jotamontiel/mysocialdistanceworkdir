from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact, name="contact"),
    path('contactMap_display/', views.contactMapDisplayView, name="contactMap_display"),
]