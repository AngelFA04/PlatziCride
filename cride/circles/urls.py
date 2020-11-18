"""Circles URLS."""

# Django
from django.urls import path, include

# DRF
from rest_framework.routers import DefaultRouter

# Views
from cride.circles.views import circles
from cride.circles.views import memberships as membership_views

router = DefaultRouter()
router.register(r'circles',circles.CircleViewSet, basename='circle')
router.register(r'circles/(?P<slug_name>[a-zA-Z0-9_-]+)/members',
                membership_views.MembershipViewSet,
                basename='membership')

urlpatterns = [
    path('', include(router.urls))
]
