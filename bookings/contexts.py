"""
Context processor.
Its purpose is to make this dictionary available
to all templates across the entire application
Much like you can use request.user in any template
due to the presence of the built-in request context processor.
"""
from django.shortcuts import get_object_or_404
from therapy.models import Therapy


def booking_contents(request):

    # An empty list for the booked sessions to live in
    booking_items = []
    total = 0
    therapy_sessions = 0

    # Retrieve the 'booking' from the session
    # or create an empty dictionary {} if it does not exist
    booking = request.session.get("booking", {})

    # In order to populate the values of the variables :
    # . booking_items
    # . total
    # . therapy_sessions
    # We need to iterate through all the items in the booking.
    # And along the way, tally up the total cost and number of sessions.
    # And add the therapies and their data to the booking items list.
    # So we can display them on the booking page.
    # And elsewhere throughout the site.

    # First variable is the key from the booking item (we call it 'therapy_id')
    # Second variable is the value of that key
    # (we are calling it 'number_sessions')
    for therapy_id, number_sessions in booking.items():
        # For each therapy id and number of sessions in booking.items.

        # First get the therapy.
        therapy = get_object_or_404(Therapy, pk=therapy_id)

        # Add number of sessions times the price to the total
        total += number_sessions * therapy.price

        # Increment the number of sessions for this therapy
        # by the number of sessions.
        therapy_sessions += number_sessions

        # Add a dictionary to the list of booking items
        #  containing not only the id and the number of sessions,
        # but also the Therapy object itself.
        # That will give us access to all the other fields,
        #  such as the image and so on,
        # when iterating through the booking items in our templates.
        booking_items.append(
            {
                "therapy_id": therapy_id,
                "number_sessions": number_sessions,
                "therapy": therapy,
            }
        )

    grand_total = total

    # This context concept is the same as
    # the context we've been using in our views
    # the only difference is we're returning it directly
    # and making it available to
    # all templates by putting it in settings.py
    # Add all these items to the context.
    # So they'll be available in templates across the site.
    context = {
        "booking_items": booking_items,
        "total": total,
        "therapy_sessions": therapy_sessions,
        "grand_total": grand_total,
    }

    return context
