"""Circle membership views"""

# DRF
from rest_framework import viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from cride.circles.models import Circle, Membership, Invitation

# Permissions
from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsActiveCircleMember, IsAdminOrMembershipOwner, IsSelfMember
# Serializers
from cride.circles.serializers import MembershipModelSerializer, AddMemberSerializer

class MembershipViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin):
    """ Circle membership viewset."""

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists"""
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permissions based on actions."""
        permissions = [IsAuthenticated]
        if self.action != 'create':
            permissions.append(IsActiveCircleMember)
        if self.action == 'destroy':
            permissions.append(IsAdminOrMembershipOwner)
        if self.action == 'invitations':
            permissions.append(IsSelfMember)
        return [p() for p in permissions]

    def get_queryset(self):
        """Return circle members"""
        return Membership.objects.filter(circle=self.circle, is_active=True)

    def get_object(self):
        """Return the circle membership by using the user's username."""
        # import pdb; pdb.set_trace()
        return get_object_or_404(Membership, user__username=self.kwargs['pk'],
                                 circle=self.circle,
                                 is_active=True)

    def perform_destroy(self, instance):
        """Disable membership"""
        instance.is_active = False
        instance.save()

    def create(self, request, *args, **kwargs):
        """Handle member creation from invitation code."""
        serializer = AddMemberSerializer(
            data=request.data,
            context={'circle': self.circle, 'request': request}
        )

        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=['get'])
    def invitations(self, request, *args, **kwargs):
        """Retrieve a member's invitations breakdown.

        Will return a list containing all the members that have
        used its invitations and another list containing the
        invitations that haven't used yet.
        """
        member = self.get_object()
        invited_members = Membership.objects.filter(
            circle=self.circle,
            invited_by=request.user,
            is_active=True
        )

        unused_invitations = Invitation.objects.filter(
            used=False,
            circle=self.circle,
            issued_by=request.user
        ).values_list('code')

        diff = member.remaining_invitations - len(unused_invitations)
        invitations = [x[0] for x in unused_invitations]

        # Append the codes that haven't been used
        for i in range(0, diff):
            invitations.append(
                Invitation.objects.create(
                    issued_by=request.user,
                    circle=self.circle
                    ).code
                )

        data = {
            'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
            'invitations': invitations
        }


        return Response(data)
