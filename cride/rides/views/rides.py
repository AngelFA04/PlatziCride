# DRF
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

# Serializers
from cride.rides.serializers import CreateRideSerializer, RideModelSerializer

# Filters
from rest_framework.filters import SearchFilter, OrderingFilter

# Permissions
from cride.circles.permissions import IsActiveCircleMember
from cride.rides.permissions import IsRideOwner

# Models
from cride.circles.models import Circle

# Utils
from django.utils import timezone
from datetime import timedelta
class RideViewSets(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):

    """Ride view set."""

    permission_classes = [IsAuthenticated, IsActiveCircleMember]
    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ('departure_date', 'arrival_date', 'available_seats')
    ordering_fields = ('departure_date', 'arrival_date', 'available_seats')
    search_fields = ('departure_location', 'arrival_location')

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSets, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permission based on action."""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsRideOwner)

        return [p() for p in permissions]

    def get_serializer_context(self):
        context = super(RideViewSets, self).get_serializer_context()
        context['circle'] = self.circle

        return context

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateRideSerializer

        return RideModelSerializer

    def get_queryset(self):
        """Return active circles rides."""
        offset = timezone.now() + timedelta(minutes=10)

        return  self.circle.ride_set.filter(
            departure_date__gte=offset,
            is_active=True,
            available_seats__gte=1,
        )
