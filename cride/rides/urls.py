"""Rides URLS."""

# Django
from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# Views
from cride.rides import views as ride_views

router = DefaultRouter()
router.register(r'circles/(?P<slug_name>[a-zA-Z0-9_-]+)/rides',
                ride_views.RideViewSets,
                basename='ride')

urlpatterns = [
    path('', include(router.urls))
]
