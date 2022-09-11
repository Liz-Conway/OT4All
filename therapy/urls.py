from django.urls import path
from .views import AllTherapies

urlpatterns = [
    path("", AllTherapies.as_view(), name="therapies"),
]
