from django.views.generic.base import TemplateView
from django.core.files import temp
from .models import Meeja, Meeja2
from django.shortcuts import render

# Create your views here.
class HomePage(TemplateView):
    """A class for rendering the home page"""

    template_name = "home/index.html"

    # TemplateView does not need to define get() method


class MeejaPage(TemplateView):
    template_name = "home/meeja.html"

    def get(self, request, *args, **kwargs):
        all_pictures = Meeja.objects.all()

        context = {"pictures": all_pictures}

        return render(request, self.template_name, context)


class MeejaPage2(TemplateView):
    template_name = "home/meeja2.html"

    def get(self, request, *args, **kwargs):
        all_pictures = Meeja2.objects.all()

        context = {"pictures": all_pictures}

        return render(request, self.template_name, context)
