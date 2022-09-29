from django.views.generic.base import TemplateView
from .models import Testimonial
from .forms import TestimonialForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls.base import reverse


class Testimonials(TemplateView):
    """A class for rendering a page containing all testimonials"""

    template_name = "testimonials/testimonials.html"

    # TemplateView does not need to define get() method
    # But here we need to tell the page what Testimonials to show
    def get_context_data(self, **kwargs):
        all_testimonials = Testimonial.objects.all()

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["testimonials"] = all_testimonials

        return context


class AddTestimonial(TemplateView):
    """A class for allowing a client to add a testimonial"""

    template_name = "testimonials/add-testimonial.html"

    def post(self, request, *args, **kwargs):
        # Instantiate a new instance of the TherapyForm from request.POST and
        # include request .FILES also in order to make sure to capture
        # the image of the therapy if one was submitted
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your testimonial has been added.\nThank You!"
            )
            return redirect(reverse("testimonials"))
        else:
            # Attach a generic error message
            # telling the user to check their form
            # which will display the errors.
            messages.error(
                request,
                "Failed to add your Testimonial.  Please ensure the form is valid.",
            )
            context = {"form": form}

            return render(request, self.template_name, context)
