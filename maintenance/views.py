from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from therapy.models import Therapy, Style
from django.contrib import messages
from django.urls.base import reverse
from .forms import TherapyForm


class AddTherapy(TemplateView):
    """
    A view to allow Admin users to add a therapy to the store
    """

    template_name = "maintenance/add-therapy.html"

    def get_context_data(self, **kwargs):
        form = TherapyForm()
        context = {"form": form}

        return context

    def post(self, request):
        # Instantiate a new instance of the TherapyForm from request.POST and
        # include request .FILES also in order to make sure to capture
        # the image of the product if one was submitted
        form = TherapyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added new Therapy!")
            return redirect(reverse("addTherapy"))
        else:
            # Attach a generic error message telling the user to check their form
            # which will display the errors.
            messages.error(
                request,
                "Failed to add Therapy.  Please ensure the form is valid.",
            )
            context = {"form": form}

            return render(request, self.template_name, context)


class ListTherapies(TemplateView):
    """
    A view to allow Admin users to view the therapies that are in the store
    """

    template_name = "maintenance/list-therapies.html"
    # template_name = "home/index.html"
    # template_name = "therapy/therapies.html"

    def get_context_data(self, **kwargs):
        print("In get_context_data)_")
        therapies = Therapy.objects.all()
        print("Got therapies")
        print(therapies)
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        print("Got super context")
        print(context)
        context["therapies"] = therapies
        print(context)
        print("Set therapies in the context")
        print("Returning the context")

        return context
