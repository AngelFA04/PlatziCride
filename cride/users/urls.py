"""User URLS."""

# Django
from django.urls import path, include

# DRF
from rest_framework import routers


# Views
from cride.users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users',UserViewSet, basename='user')

urlpatterns = [
    path('',include(router.urls)),
]
