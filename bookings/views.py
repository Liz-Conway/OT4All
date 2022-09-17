from django.views.generic.base import TemplateView
from django.shortcuts import redirect

# Create your views here.
class BookingsContents(TemplateView):
    """A class for rendering the bookings contents page"""

    template_name = "bookings/bookings.html"


class AddToBookings(TemplateView):
    """
    Book a number of sessions for a specific therapy
    """

    def post(self, request, therapy_id):

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
        # tries to get the booking stored in the HTTP session - if it already exists,
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
        else:
            # This therapy has not been booked (does not exist).
            # Create a key for the therapy in our dictionary,
            # and set its value to the number of therapy sessions booked.
            booking[therapy_id] = therapy_sessions

        # Put the booking variable into the HTTP session.
        #  Which itself is just a python dictionary.
        request.session["booking"] = booking

        # Post/Redirect/Get (PRG) pattern - a web development design pattern
        # After a POST, redirect to another page which is loaded using HTTP GET protocol
        # This avoids ill effects, such as submitting the form another time.
        # I.E. The form will never be POSTed twice in a row.
        return redirect(redirect_url)
