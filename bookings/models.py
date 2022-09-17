from django.db import models


class Booking(models.Model):

    # "editable=False" attribute on the booking number field.
    # We're gonna automatically generate this booking number.
    # And we'll want it to be unique and permanent
    # so users can find their previous bookings.
    booking_number = models.CharField(
        max_length=32, null=False, editable=False
    )
