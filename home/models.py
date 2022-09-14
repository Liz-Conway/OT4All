from django.db import models
from cloudinary.models import CloudinaryField


class Meeja(models.Model):
    my_image = models.ImageField(upload_to="ot4u", blank=True)
    name = models.CharField(max_length=25)


class Meeja2(models.Model):
    my_image = CloudinaryField("image", default="placeholder")
    name = models.CharField(max_length=25)
