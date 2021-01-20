from django.contrib import admin
from django.urls import path
from .views import NYTMenuPageView

urlpatterns = [
    path('nytimes_display/', NYTMenuPageView.as_view(), name="nytimes_display"),
]