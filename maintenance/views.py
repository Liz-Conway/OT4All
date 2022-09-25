from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView, View
from therapy.models import Therapy
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
        # the image of the therapy if one was submitted
        form = TherapyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully added new Therapy!")
            return redirect(reverse("addTherapy"))
        else:
            # Attach a generic error message
            # telling the user to check their form
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

    def get_context_data(self, **kwargs):
        therapies = Therapy.objects.all()
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["therapies"] = therapies

        return context


class EditTherapy(TemplateView):
    """
    A view to allow Admin users to edit an existing therapy
    """

    template_name = "maintenance/edit-therapy.html"

    def get_context_data(self, **kwargs):
        try:
            therapy = Therapy.objects.get(pk=kwargs["therapy_id"])
            form_data = {
                "name": therapy.name,
                "style": therapy.style,
                "description": therapy.description,
                "price": therapy.price,
                "image": therapy.image,
                "course_sessions": therapy.course_sessions,
                "location": therapy.location,
                "extra_requirements": therapy.extra_requirements,
            }

            try:
                form = TherapyForm(self.request.FILES, form_data)
            except Exception as formEx:
                messages.error(f"Form Error :  {formEx.message}")
            # Call the base implementation first to get a context
            context = super().get_context_data(**kwargs)
            context["form"] = form
            context["therapy"] = therapy
        except Exception as ex:
            messages.error(f"Error : {ex.message}")

        return context

    def post(self, request, *args, **kwargs):
        therapy = get_object_or_404(Therapy, pk=kwargs.get("therapy_id"))

        # Create a new instance of the TherapyForm using the POST data.
        # Tell it the instance we're updating
        # is the therapy we've just retrieved above
        form = TherapyForm(request.POST, request.FILES, instance=therapy)

        if form.is_valid():
            form.save()
            messages.success(request, "Therapy updated successfully")
            return redirect(reverse("listTherapies"))
        else:
            # Attach a generic error message
            # telling the user to check their form
            # which will display the errors.
            messages.error(
                request,
                "Failed to add therapy.  Please ensure the form is valid.",
            )

        context = {"form": form}

        return render(request, self.template_name, context)


class DeleteTherapy(View):
    """
    A view to allow Admin users to delete an existing therapy
    """

    def post(self, request, *args, **kwargs):
        therapy_id = kwargs.get("therapy_id")
        try:
            # Remove the chosen therapy from the database
            to_delete = Therapy.objects.get(pk=therapy_id)
            delete_name = to_delete.name
            to_delete.delete()
            messages.success(
                self.request, f"{delete_name} was successfully removed"
            )
        except Therapy.DoesNotExist as dne:
            messages.error(self.request, dne.message)
        except Exception as ex:
            messages.error(self.request, f"Exception :  {ex.message}")

        return redirect(reverse("listTherapies"))
