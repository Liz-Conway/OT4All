from django.views.generic.base import TemplateView
from therapy.models import Therapy
from django.shortcuts import render


# Create your views here.
class AllTherapies(TemplateView):
    """A class for rendering a page containing all available therapies"""

    template_name = "therapy/therapies.html"

    # TemplateView does not need to define get() method
    # But here we need to tell the page what Therapies to show so we will
    def get(self, request, *args, **kwargs):
        all_therapies = Therapy.objects.all()

        context = {
            "therapies": all_therapies,
        }

        return render(request, self.template_name, context)
