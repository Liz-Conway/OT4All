from django.views.generic.base import TemplateView
from .models import Testimonial


class Testimonials(TemplateView):
    """A class for rendering a page containing all available therapies"""

    template_name = "testimonials/testimonials.html"

    # TemplateView does not need to define get() method
    # But here we need to tell the page what Testimonials to show so we will
    def get_context_data(self, **kwargs):
        all_testimonials = Testimonial.objects.all()

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["testimonials"] = all_testimonials

        return context
