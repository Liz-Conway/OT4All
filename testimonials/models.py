from django.db import models


class Testimonial(models.Model):

    first_name = models.CharField(max_length=25, null=False, blank=False)
    last_name = models.CharField(max_length=25, null=False, blank=False)
    image = models.ImageField(upload_to="ot4u", null=True, blank=True)
    testimony_title = models.CharField(max_length=60, null=True, blank=True)
    testimony = models.TextField(null=False, blank=False)
    # Use "auto_now_add" attribute on the date field
    # which will automatically set the testimonial date and time
    # whenever a new testimonial is created
    date = models.DateField(auto_now_add=True)
