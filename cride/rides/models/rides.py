"""Rides Models."""

# Django
from django.db import models

# Utilities
from cride.utils.models import CRideModel

class Ride(CRideModel):
    """ Ride model"""

    offered_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    offered_in = models.ForeignKey('circles.Circle', on_delete=models.SET_NULL, null=True)

    passengers = models.ManyToManyField('users.User', related_name='passengers')

    available_seats = models.PositiveSmallIntegerField(default=1)
    comments = models.TextField(blank=True)

    departure_location = models.CharField(verbose_name='Start location wof the ride', max_length=250)
    departure_date = models.DateTimeField(verbose_name='Starting hour of the ride')

    arrival_location = models.CharField(verbose_name='End location of the ride', max_length=250)
    arrival_date = models.DateTimeField(verbose_name='Ending hour of the ride')

    rating = models.FloatField(null=True)

    is_active = models.BooleanField('active status', default=True,
                                    help_text='Used for disabling the ride or marking it as finished')

    def __str__(self):
        """Return ride details."""
        return f'{self.departure_location} to {self.arrival_location} | {self.departure_date} - {self.arrival_date}'
