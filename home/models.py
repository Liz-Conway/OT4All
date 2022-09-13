from django.db import models


class Meeja(models.Model):
    my_image = models.ImageField(upload_to="ot4u", blank=True)
    name = models.CharField(max_length=25)
