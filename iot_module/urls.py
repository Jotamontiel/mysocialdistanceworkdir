from django.contrib import admin
from django.urls import path
from .views import IotModuleDashboardView, IotModuleProfileCreateAuxView, IotModuleComponentListView, IotModuleComponentDetailView, IotModuleComponentCreateView, IotModuleComponentUpdateView, IotModuleComponentDeleteView

urlpatterns = [
    path('iotmodule_dashboard_display/', IotModuleDashboardView.as_view(), name="iotmodule_dashboard_display"),
    path('iotmodule_profilecreateaux_display/', IotModuleProfileCreateAuxView.as_view(), name='iotmodule_profilecreateaux_display'),
    path('iotmodule_componentlist_display/', IotModuleComponentListView.as_view(), name="iotmodule_componentlist_display"),
    path('iotmodule_componentdetail_display/<int:pk>/<slug:slug>/', IotModuleComponentDetailView.as_view(), name='iotmodule_componentdetail_display'),
    path('iotmodule_componentcreate_display/', IotModuleComponentCreateView.as_view(), name='iotmodule_componentcreate_display'),
    path('iotmodule_componentupdate_display/<int:pk>/<slug:slug>/', IotModuleComponentUpdateView.as_view(), name='iotmodule_componentupdate_display'),
    path('iotmodule_componentdelete_display/<int:pk>/', IotModuleComponentDeleteView.as_view(), name='iotmodule_componentdelete_display'),
]