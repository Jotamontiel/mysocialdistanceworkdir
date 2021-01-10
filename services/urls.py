from .views import ServicesListView
from django.urls import path

urlpatterns = [
    path('services/', ServicesListView.as_view(), name='services'),
]