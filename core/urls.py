from django.urls import path
from .views import HomePageView, InfoPageView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('info/', InfoPageView.as_view(), name="info"),
    path('cmd_display/', views.cmdDisplayView, name="cmd_display"),
    path('city3D_display/', views.city3DDisplayView, name="city3D_display"),
    path('timeLine_display/', views.timeLineDisplayView, name="timeLine_display"),
]