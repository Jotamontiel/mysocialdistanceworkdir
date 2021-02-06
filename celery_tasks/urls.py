from django.contrib import admin
from django.urls import path
from .views import HackerNewsDashboardView, SpotifySearchView, NYTMenuPageView

urlpatterns = [
    path('nytimes_display/', NYTMenuPageView.as_view(), name="nytimes_display"),
    path('hackernewsdashboard_display/', HackerNewsDashboardView.as_view(), name="hackernewsdashboard_display"),
    path('spotifysearch_display/', SpotifySearchView.as_view(), name="spotifysearch_display"),
]