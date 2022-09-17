from django.views.generic.base import TemplateView

# Create your views here.
class BookingsContents(TemplateView):
    """A class for rendering the bookings contents page"""

    template_name = "bookings/bookings.html"
