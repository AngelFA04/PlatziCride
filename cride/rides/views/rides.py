# DRF
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

# Serializers
from cride.rides.serializers import CreateRideSerializer

# Permissions
from cride.circles.permissions import IsActiveCircleMember

# Models
from cride.circles.models import Circle

class RideViewSets(mixins.CreateModelMixin, viewsets.GenericViewSet):

    """Ride view set."""

    serializer_class =  CreateRideSerializer
    permission_classes = [IsAuthenticated, IsActiveCircleMember]

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(RideViewSets, self).dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super(RideViewSets, self).get_serializer_context()
        context['circle'] = self.circle

        return context
