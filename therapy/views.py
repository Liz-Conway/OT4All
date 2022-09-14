from django.views.generic.base import TemplateView
from therapy.models import Therapy
from django.shortcuts import render, get_object_or_404


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


class SingleTherapy(TemplateView):
    """
    A view to show all details for an individual therapy
    """

    template_name = "therapy/therapy-details.html"

    def get(self, request, therapy_id):
        single_therapy = get_object_or_404(Therapy, pk=therapy_id)

        context = {
            "therapy": single_therapy,
        }

        return render(request, self.template_name, context)
