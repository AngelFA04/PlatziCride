"""Circle serializers."""

# Models
from cride.circles.models import Circle, Membership

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# Serializers
from cride.users.serializers import UserModelSerializer

class CircleSerializer(serializers.Serializer):
    """Circle serializer."""

    name = serializers.CharField()
    slug_name = serializers.SlugField()
    rides_taken = serializers.IntegerField()
    rides_offered = serializers.IntegerField()
    members_limit = serializers.IntegerField()

class CreateCircleSerializer(serializers.Serializer):
    """Create circle serializer."""

    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(
        max_length=40,
        validators=[
            UniqueValidator(queryset=Circle.objects.all())
        ]
        )
    about = serializers.CharField(max_length=255, required=False)

    def create(self, data):
        """Create circle."""
        return Circle.objects.create(**data)


class CircleModelSerializer(serializers.ModelSerializer):
    """Circle model serializer"""
    members_limit = serializers.IntegerField(
        required=False,
        min_value=10,
        max_value=32000,
    )

    is_limited = serializers.BooleanField(default=False)

    class Meta:
        model = Circle
        fields = (
            'name', 'slug_name',
            'about', 'picture', 'rides_offered',
            'rides_taken', 'verified', 'is_public',
            'is_limited', 'members_limit',
        )
        read_only_fields = ('is_public', 'verified', 'rides_offered', 'rides_taken')

    def validate(self, data):
        """Ensure both members limit and is limited are present"""
        members_limit = data.get('members_limit', None)
        is_limited = data.get('is_limited', False)
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError('If circle is limited, a member limit must be provided')
        return data
