from django.urls import path
from .views import BookingsContents, AddToBookings, UpdateBooking

urlpatterns = [
    path("", BookingsContents.as_view(), name="bookings"),
    path("add/<therapy_id>", AddToBookings.as_view(), name="book"),
    path("update/<therapy_id>", UpdateBooking.as_view(), name="updateBooking"),
]
