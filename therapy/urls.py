from django.urls import path
from .views import AllTherapies, SingleTherapy

urlpatterns = [
    path("", AllTherapies.as_view(), name="therapies"),
    path("<int:therapy_id>/", SingleTherapy.as_view(), name="singleTherapy"),
]
