from django.contrib import admin
from django.urls import path
from .views import IotModuleDashboardView

urlpatterns = [
    path('iotmodule_dashboard_display/', IotModuleDashboardView.as_view(), name="iotmodule_dashboard_display"),
]