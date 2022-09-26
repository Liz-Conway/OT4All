from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    query = models.TextField(null=False, blank=False)
