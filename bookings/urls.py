from django.urls import path
from .views import BookingsContents

urlpatterns = [
    path("", BookingsContents.as_view(), name="bookings"),
]
