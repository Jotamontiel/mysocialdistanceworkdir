from django.contrib import admin
from django.urls import path
from .views import IotModuleDashboardView, IotModuleProfileCreateAuxView, IotModuleProfileUpdateAuxView, IotModuleComponentListView, IotModuleComponentDetailView, IotModuleComponentCreateView, IotModuleComponentUpdateView, IotModuleComponentDeleteView, IotModuleProfileListView, IotModuleProfileDeleteView, IotModuleProfileDetailView, IotModuleProfileUpdateView, IotModuleUserEmailUpdateView, IotModuleProfileCreateView, IotModuleProfileDeleteAuxView, IotModuleCompanyListView, IotModuleCompanyDetailView, IotModuleCompanyDeleteView, IotModuleCompanyCreateView, IotModuleCompanyUpdateView, IotModuleCompanyEmailUpdateView, SignUpView, IotModuleComponentTypeListView, IotModuleComponentTypeCreateView, IotModuleComponentTypeUpdateView, IotModuleComponentTypeDeleteView, IotModuleComponentTypeDetailView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('iotmodule_dashboard_display/', IotModuleDashboardView.as_view(), name="iotmodule_dashboard_display"),
    path('iotmodule_useremailupdate_display/<int:pk>/<slug:slug>/<slug:flag>/', IotModuleUserEmailUpdateView.as_view(), name="iotmodule_useremailupdate_display"),
    path('iotmodule_companyemailupdate_display/<int:pk>/<slug:slug>/', IotModuleCompanyEmailUpdateView.as_view(), name="iotmodule_companyemailupdate_display"),
    path('iotmodule_profilelist_display/', IotModuleProfileListView.as_view(), name="iotmodule_profilelist_display"),
    path('iotmodule_profiledetail_display/<int:pk>/<slug:slug>/', IotModuleProfileDetailView.as_view(), name='iotmodule_profiledetail_display'),
    path('iotmodule_profilecreate_display/', IotModuleProfileCreateView.as_view(), name='iotmodule_profilecreate_display'),
    path('iotmodule_profilecreateaux_display/', IotModuleProfileCreateAuxView.as_view(), name='iotmodule_profilecreateaux_display'),
    path('iotmodule_profileupdate_display/<int:pk>/<slug:slug>/', IotModuleProfileUpdateView.as_view(), name='iotmodule_profileupdate_display'),
    path('iotmodule_profileupdateaux_display/<int:pk>/<slug:slug>/', IotModuleProfileUpdateAuxView.as_view(), name='iotmodule_profileupdateaux_display'),
    path('iotmodule_profiledelete_display/<int:pk>/', IotModuleProfileDeleteView.as_view(), name='iotmodule_profiledelete_display'),
    path('iotmodule_profiledeleteaux_display/<int:pk>/<slug:flag>/', IotModuleProfileDeleteAuxView.as_view(), name='iotmodule_profiledeleteaux_display'),
    path('iotmodule_companylist_display/', IotModuleCompanyListView.as_view(), name="iotmodule_companylist_display"),
    path('iotmodule_companydetail_display/<int:pk>/<slug:slug>/', IotModuleCompanyDetailView.as_view(), name='iotmodule_companydetail_display'),
    path('iotmodule_companycreate_display/', IotModuleCompanyCreateView.as_view(), name='iotmodule_companycreate_display'),
    path('iotmodule_companyupdate_display/<int:pk>/<slug:slug>/', IotModuleCompanyUpdateView.as_view(), name='iotmodule_companyupdate_display'),
    path('iotmodule_companydelete_display/<int:pk>/', IotModuleCompanyDeleteView.as_view(), name='iotmodule_companydelete_display'),
    path('iotmodule_componenttypeslist_display/', IotModuleComponentTypeListView.as_view(), name="iotmodule_componenttypeslist_display"),
    path('iotmodule_componenttypesdetail_display/<int:pk>/<slug:slug>/', IotModuleComponentTypeDetailView.as_view(), name='iotmodule_componenttypesdetail_display'),
    path('iotmodule_componenttypescreate_display/', IotModuleComponentTypeCreateView.as_view(), name="iotmodule_componenttypescreate_display"),
    path('iotmodule_componenttypesupdate_display/<int:pk>/<slug:slug>/', IotModuleComponentTypeUpdateView.as_view(), name='iotmodule_componenttypesupdate_display'),
    path('iotmodule_componenttypesdelete_display/<int:pk>/', IotModuleComponentTypeDeleteView.as_view(), name='iotmodule_componenttypesdelete_display'),
    path('iotmodule_componentlist_display/', IotModuleComponentListView.as_view(), name="iotmodule_componentlist_display"),
    path('iotmodule_componentdetail_display/<int:pk>/<slug:slug>/', IotModuleComponentDetailView.as_view(), name='iotmodule_componentdetail_display'),
    path('iotmodule_componentcreate_display/', IotModuleComponentCreateView.as_view(), name='iotmodule_componentcreate_display'),
    path('iotmodule_componentupdate_display/<int:pk>/<slug:slug>/', IotModuleComponentUpdateView.as_view(), name='iotmodule_componentupdate_display'),
    path('iotmodule_componentdelete_display/<int:pk>/', IotModuleComponentDeleteView.as_view(), name='iotmodule_componentdelete_display'),
]