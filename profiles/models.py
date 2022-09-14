from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    A user profile model for maintaining
     default delivery information and order history
    """

    # One-to-one field attached to the user.
    # This is just like a foreign key except that it specifies that each user can only have one profile.
    # And each profile can only be attached to one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Rest of the fields in this model are the delivery information fields we want the
    # user to be able to provide defaults for.

    # Want all these fields to be optional - null = True and blank = True for each of them
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True
    )
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True
    )
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label="Country", null=True, blank=True
    )

    def __str__(self):
        return self.user.username
