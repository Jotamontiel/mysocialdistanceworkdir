from django.urls import path
from .views import HomePageView, InfoPageView, HomeMenuPageView, AboutMenuPageView, ProjectsMenuPageView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('info/', InfoPageView.as_view(), name="info"),
    path('menu_home/', HomeMenuPageView.as_view(), name="menu_home"),
    path('menu_about/', AboutMenuPageView.as_view(), name="menu_about"),
    path('menu_projects/', ProjectsMenuPageView.as_view(), name="menu_projects"),
    path('cmd_display/', views.cmdDisplayView, name="cmd_display"),
    path('city3D_display/', views.city3DDisplayView, name="city3D_display"),
    path('timeLine_display/', views.timeLineDisplayView, name="timeLine_display"),
    path('techTree_display/', views.techTreeDisplayView, name="techTree_display"),
    path('selectAbout_display/', views.selectAboutDisplayView, name="selectAbout_display"),
]