from django.urls import path
from .views import HomePageView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('cmd_display/', views.cmdDisplayView, name="cmd_display"),
    path('city3D_display/', views.city3DDisplayView, name="city3D_display"),
]