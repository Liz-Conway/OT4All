from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.urls.base import reverse
from .forms import OrderForm


class Purchase(TemplateView):
    # The template
    template_name = "purchase/purchase.html"

    def get_context_data(self, request):
        booking = request.session.get("booking", {})

        # Bookings are empty
        if not booking:
            messages.error(request, "You have no bookings")
            # This will prevent people from manually accessing the URL
            # by typing "/purchase"
            return redirect(reverse("therapy"))

        # An instance of our order form - which will be empty for now.
        order_form = OrderForm()
        # Context containing the order form.
        context = {
            "order_form": order_form,
        }

        return context
