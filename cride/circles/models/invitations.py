"""Invitations models"""

# Django
from django.db import models

# Models
from cride.users.models import User

# Managers
from cride.circles.managers import InvitationManager

class Invitation(models.Model):

    code = models.CharField(max_length=50, unique=True)

    issued_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        help_text='Circle member that is providing the invitation',
        related_name='issued_by')

    used_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        help_text='User that used the code to enter the circlo',
        related_name='used_by')


    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE)
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True)

    # Manager
    objects = InvitationManager()

    def __str__(self):
        """Return code and circle"""
        return f'#{self.circle.slug_name}: {self.code}'
