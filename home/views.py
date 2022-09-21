from django.views.generic.base import TemplateView


class HomePage(TemplateView):
    """A class for rendering the home page"""

    template_name = "home/index.html"

    # TemplateView does not need to define get() method
