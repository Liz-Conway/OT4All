from django.views.generic.base import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.urls.base import reverse
from django.http.response import HttpResponse
from therapy.models import Therapy
from django.contrib import messages


class BookingsContents(TemplateView):
    """A class for rendering the bookings contents page"""

    template_name = "bookings/bookings.html"


class AddToBookings(TemplateView):
    """
    Book a number of sessions for a specific therapy
    """

    def post(self, request, therapy_id):

        therapy = Therapy.objects.get(pk=therapy_id)
        # Get the number of sessions from the form.
        # Convert it to an integer
        # since it'll come from the template as a string.
        therapy_sessions = int(request.POST.get("sessions"))

        # Get the redirect URL from the form so we know
        # where to redirect once the process here is finished.
        # E.G. Back to Single Therapy page
        redirect_url = request.POST.get("redirectUrl")

        # Every request-response cycle between the server and the client,
        # (In our case between the django view on the server-side
        #  and our form making the request on the client-side.)
        #  uses a HTTP session, to allow information to be stored
        #  until the client and server are done communicating.
        # This allows us to store the contents of the bookings
        # in the HTTP session,
        #  while the user browses the site and adds
        # therapy sessions to be booked.
        # By storing the bookings in the HTTP session,
        # it will persist until the user closes their browser
        #  so that they can add something to the bookings,
        # then browse to a different part of the site add something else
        # and so on without losing the their bookings..

        # The variable booking accesses the request's HTTP session,
        # tries to get the booking stored in the HTTP session
        # - if it already exists,
        # and initialises it to an empty dictionary {} if it doesn't.
        # First check to see if there's a booking variable in the HTTP session,
        # and if not this code will create one
        booking = request.session.get("booking", {})

        if therapy_id in list(booking.keys()):
            # If the therapy is already booked
            # (if there's already a key in the booking dictionary
            #  matching this therapy id)
            # then increment its number of therapy sessions
            booking[therapy_id] += therapy_sessions
            messages.success(
                request,
                f"Updated {therapy.name} sessions to {booking[therapy_id]}",
            )
        else:
            # This therapy has not been booked (does not exist).
            # Create a key for the therapy in our dictionary,
            # and set its value to the number of therapy sessions booked.
            booking[therapy_id] = therapy_sessions
            messages.success(request, f"You booked Therapy {therapy.name}")

        # Put the booking variable into the HTTP session.
        #  Which itself is just a python dictionary.
        request.session["booking"] = booking

        # Post/Redirect/Get (PRG) pattern - a web development design pattern
        # After a POST, redirect to another page
        # which is loaded using HTTP GET protocol
        # This avoids ill effects, such as submitting the form another time.
        # I.E. The form will never be POSTed twice in a row.
        return redirect(redirect_url)


class UpdateBooking(TemplateView):
    """
    Adjust the number of sessions of a particular therapy
    to the specified amount
    """

    def post(self, request, therapy_id):

        therapy = get_object_or_404(Therapy, pk=therapy_id)
        # Get the number of sessions from the form.
        # Convert it to an integer
        # since it'll come from the template as a string.
        number_of_sessions = int(request.POST.get("sessions"))

        # No need for a  redirect URL
        # Since we alway want to redirect back to the Bookings page

        # Every request-response cycle between the server and the client,
        # (In our case between the django view on the server-side
        #  and our form making the request on the client-side.)
        #  uses a HTTP session, to allow information to be stored
        #  until the client and server are done communicating.
        # This allows us to store the contents of the Booking
        # in the HTTP session,
        #  while the user browses the site and adds therapies to be purchased.
        # By storing the Booking in the session,
        # it will persist until the user closes their browser
        #  so that they can add something to the booking,
        # then browse to a different part of the site add something else
        # and so on without losing their previous bookings.

        # The variable bookings accesses the requests session,
        # tries to get the bookings stored in the session
        # - if it already exists,
        # and initialises it to an empty dictionary {} if it doesn't.
        # First check to see if there's a bookings variable in the session,
        # and if not this code will create one
        bookings = request.session.get("booking", {})

        # Basic idea :
        # If number_of_sessions > zero, Set the therapy's sessions accordingly
        #  Otherwise we'll just remove the therapy.
        if number_of_sessions > 0:
            # Set the therapy's number of sessions to the updated value
            bookings[therapy_id] = number_of_sessions
            messages.success(
                request,
                f"Updated {therapy.name} number of sessions to {bookings[therapy_id]}",
            )
        else:
            # Remove the therapy entirely by using the pop() function
            bookings.pop(therapy_id)
            messages.success(
                request, f"Removed {therapy.name} from your bookings"
            )

        # Put the bookings variable into the session.
        #  Which itself is just a python dictionary.
        request.session["booking"] = bookings

        # Redirect back to the view bookings URL
        return redirect(reverse("bookings"))


class RemoveBooking(TemplateView):
    """
    Remove the therapy from the bookings
    """

    def post(self, request, therapy_id):

        # No need for a  redirect URL
        # Since we alway want to redirect back to the Bookings page

        # Wrap this entire block of code in a try block.
        try:
            therapy = get_object_or_404(Therapy, pk=therapy_id)
            # Every request-response cycle between the server and the client,
            # (In our case between the django view on the server-side
            #  and our form making the request on the client-side.)
            #  uses a HTTP session, to allow information to be stored
            #  until the client and server are done communicating.
            # This allows us to store the contents of the booking
            # in the HTTP session,
            #  while the user browses the site
            # and adds therapies to be purchased.
            # By storing the bookings in the HTTP session,
            # it will persist until the user closes their browser
            #  so that they can add something to the bookings,
            # then browse to a different part of the site add something else
            # and so on without losing the contents of their bookings.

            # The variable bookings accesses the requests HTTP session,
            # tries to get the booking stored in the HTTP session
            # - if it already exists,
            # and initialises it to an empty dictionary {} if it doesn't.
            # First check to see if there's a booking variable in the session,
            # and if not this code will create one
            bookings = request.session.get("booking", {})

            # Removing the therapy is as simple
            # as popping it out of the booking
            bookings.pop(therapy_id)
            messages.success(
                request, f"Removed {therapy.name} from your bookings"
            )

            # Put the bookings variable into the HTTP session.
            #  Which itself is just a python dictionary.
            request.session["booking"] = bookings

            # Since this view will be posted to from a JavaScript function.
            # Return a 200 HTTP response.
            # Implying that the therapy was successfully removed
            return HttpResponse(status=200)
        # Catch any exceptions that happen
        # in order to return a 500 server error
        except Exception as ex:
            messages.error(request, f"Error removing therapy :  {ex}")
            return HttpResponse(status=500)
