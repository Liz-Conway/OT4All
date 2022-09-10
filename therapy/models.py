from django.db import models


class Style(models.Model):
    name = models.CharField(max_length=254)
    equipment = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Therapy(models.Model):
    style = models.ForeignKey(
        "Style", null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=3, decimal_places=0)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    course_sessions = models.PositiveIntegerField(
        editable=False,
        help_text="The recommended number of sessions for this particular therapy.",
    )
    location = models.CharField(max_length=254)
    extra_requirements = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
