""" Memberships permission classes"""

# DRF
from rest_framework.permissions import BasePermission

# Models
from cride.circles.models import Membership, Invitation

class IsActiveCircleMember(BasePermission):
    """Allow access only to circle members

    Expected that views implementing this permission
    have a `circle` attribute assigned
    """

    def has_permission(self, request, view):
        """Verify that user is an active member of the circle"""
        circle = view.circle
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True

class IsAdminOrMembershipOwner(BasePermission):
    """
    Allow accese only to (Circle's admin) or users
    that are owner of the membership (object).
    """

    def has_permission(self, request, view):
        membership = view.get_object()
        if membership.user == request.user:
            return True

        try:
            Membership.objects.get(
                circle=view.circle,
                user=request.user,
                is_active=True,
                is_admin=True
            )
        except Membership.DoesNotExist:
            return False
        return True


# class IsSelfMember(BasePermission):
#     """Allow access only to the invitation owner"""

#     def has_object_permission(self, request, view, obj):
#         """Verify user is owner of invitation in the obj."""
#         try:
#             Invitation.objects.get(
#                 issued_by=request.user,
#                 circle=obj
#             )
#         except Invitation.DoesNotExist:
#             return False
#         return True
#     pass


class IsSelfMember(BasePermission):
    """Allow access only to the invitation owner"""

    def has_permission(self, request, view):
        """Let object permission grant access."""
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """Verify user is owner of invitation in the obj."""

        return request.user == obj.user
