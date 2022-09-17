from django.urls import path
from .views import BookingsContents, AddToBookings

urlpatterns = [
    path("", BookingsContents.as_view(), name="bookings"),
    path("add/<therapy_id>", AddToBookings.as_view(), name="book"),
]
