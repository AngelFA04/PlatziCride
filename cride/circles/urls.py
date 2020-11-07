"""Circles URLS."""

# Django
from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# Views
from cride.circles.views import circles

router = DefaultRouter()
router.register(r'circles',circles.CircleViewSet, basename='circle')


urlpatterns = [
    path('', include(router.urls))
]
