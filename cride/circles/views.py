"""Circles views."""

# Django REST Framework
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Models
from cride.circles.models import Circle

# Serializers
from cride.circles.serializers import CircleSerializer, CreateCircleSerializer

@api_view(['GET'])
def list_circles(request):
    """List circles."""
    # import pdb; pdb.set_trace()
    circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(circles, many=True)
    # print(serializer.data)
    return Response(serializer.data)

@api_view(['POST'])
def create_circle(request):
    """Create circle."""
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    #data=serializer.data
    circle = serializer.save()
    return Response(CircleSerializer(circle).data)
