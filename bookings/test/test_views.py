"""
@author: liz
"""
from django.test import TestCase, Client
from therapy.models import Therapy, Style
from django.urls.base import reverse
from datetime import datetime
from django.contrib.messages.api import get_messages


class BookingViewsTest(TestCase):
    def setUp(self):
        self.style = Style.objects.create(name="Test Style")
        self.therapy = Therapy.objects.create(
            name="Test Therapy",
            description="A test therapy for use in unit testing",
            price=100,
            course_sessions=3,
            style=self.style,
        )

        self.bookings_url = reverse("bookings")
        self.add_booking_url = reverse("book", args=[self.therapy.id])
        self.remove_booking_url = reverse(
            "removeBooking", args=[self.therapy.id]
        )
        self.update_booking_url = reverse(
            "updateBooking", args=[self.therapy.id]
        )

    def test_show_bookings_page(self):
        response = self.client.get(self.bookings_url)

        self.assertEqual(
            response.status_code,
            200,
            "Going to 'Bookings' page should return a Status Code of 200 (OK)",
        )
        self.assertTemplateUsed(
            response,
            "bookings/bookings.html",
            "Bookings page should use the bookings.html template",
        )
        bookings = self.client.session.get("booking")

        self.assertEquals(
            bookings,
            None,
            "No Bookings should be made when first entering Booking Cart",
        )

    def test_post_add_booking(self):
        book_sessions = 5
        booking_data = {
            "sessions": book_sessions,
        }

        response = self.client.post(
            f"bookings/add/{self.therapy.id}", booking_data
        )
        # messages = list(response.context['messages'])
        booking = self.client.session.get("booking")

        self.assertNotEqual(
            booking, None, "There should be a booking in the HTTP Session"
        )

        self.assertEqual(
            response.status_code,
            302,
            "Posting the Add Booking form should\
             return a Status Code of 302 (OK)",
        )

        booked_sessions = booking.get(self.therapy.id)

        self.assertEqual(
            book_sessions, booked_sessions, "There should be 5 booked sessions"
        )

    def test_post_update_booking(self):
        book_sessions = 5
        booking_data = {
            "sessions": book_sessions,
        }

        response = self.client.post(
            f"bookings/add/{self.therapy.id}", booking_data
        )
        # messages = list(response.context['messages'])
        booking = self.client.session.get("booking")

        self.assertNotEqual(
            booking, None, "There should be a booking in the HTTP Session"
        )

        self.assertEqual(
            response.status_code,
            302,
            "Posting the Add Booking form should\
             return a Status Code of 302 (OK)",
        )

        booked_sessions = booking.get(self.therapy.id)

        self.assertEqual(
            5, booked_sessions, "There should be 5 booked sessions"
        )

        updated_sessions = {"sessions": 10}

        response = self.client.post(
            f"bookings/update/{self.therapy.id}", updated_sessions
        )
        booking = self.client.session.get("booking")

        self.assertEqual(
            response.status_code,
            302,
            "Posting the Add Booking form should\
             return a Status Code of 302 (OK)",
        )

        booked_sessions = booking.get(self.therapy.id)

        self.assertEqual(
            10, booked_sessions, "There should be 10 booked sessions"
        )

    def test_post_remove_booking(self):
        book_sessions = 5
        booking_data = {
            "sessions": book_sessions,
        }

        response = self.client.post(
            f"bookings/add/{self.therapy.id}", booking_data
        )
        # messages = list(response.context['messages'])
        booking = self.client.session.get("booking")

        self.assertNotEqual(
            booking, None, "There should be a booking in the HTTP Session"
        )

        self.assertEqual(
            response.status_code,
            302,
            "Posting the Update Booking form should\
             return a Status Code of 302 (OK)",
        )

        booked_sessions = booking.get(self.therapy.id)

        self.assertEqual(
            5, booked_sessions, "There should be 5 booked sessions"
        )

        response = self.client.post(self.remove_booking_url)
        booking = self.client.session.get("booking")

        self.assertEqual(
            response.status_code,
            302,
            "Posting the Remove Booking form should\
             return a Status Code of 302 (OK)",
        )

        booked_sessions = booking.get(self.therapy.id)

        self.assertEqual(
            None,
            booked_sessions,
            "There should be NO booked sessions for this therapy ID",
        )
