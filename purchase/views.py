from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.urls.base import reverse
from .forms import OrderForm


class Purchase(TemplateView):
    # The template
    template_name = "purchase/purchase.html"

    def get(self, request, *args, **kwargs):
        booking = request.session.get("booking", {})

        # Bookings are empty
        if not booking:
            messages.error(request, "You have no bookings")
            # This will prevent people from manually accessing the URL
            # by typing "/purchase"
            return redirect(reverse("therapies"))

        # An instance of our order form - which will be empty for now.
        order_form = OrderForm()
        # Context containing the order form.
        context = {
            "order_form": order_form,
            "stripe_public_key": "pk_test_51LTZcpIYwD1Sv5tNNF2yHlPgyxmjvxChh3i4eBhb1ISyZq7NjNDJzFeRgWDmf0thkPkDkN5g7IvXQ1kYVJ1N7pDg008nH17kl8",
            "client_secret": "Test client secret",
        }

        return render(request, self.template_name, context)
