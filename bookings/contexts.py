"""
Context processor.
Its purpose is to make this dictionary available 
to all templates across the entire application
Much like you can use request.user in any template
due to the presence of the built-in request context processor.
"""


def booking_contents(request):

    # An empty list for the booked sessions to live in
    booking_items = []
    total = 0
    therapy_count = 0

    grand_total = total

    # This context concept is the same as the context we've been using in our views
    # the only difference is we're returning it directly and making it available to
    # all templates by putting it in settings.py
    # Add all these items to the context.
    # So they'll be available in templates across the site.
    context = {
        "booking_items": booking_items,
        "total": total,
        "therapy_count": therapy_count,
        "grand_total": grand_total,
    }

    return context
