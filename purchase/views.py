from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.contrib import messages
from django.urls.base import reverse
from .forms import OrderForm
from bookings.contexts import booking_contents
from ot4u.settings import (
    STRIPE_PUBLIC_KEY,
    STRIPE_SECRET_KEY,
    STRIPE_CURRENCY,
)

import stripe
from therapy.models import Therapy
from .models import Order, OrderLineItem
from django.http.response import HttpResponse
import json
from django.conf import settings


class Purchase(TemplateView):
    # The template
    template_name = "purchase/purchase.html"

    def get(self, request, *args, **kwargs):
        stripe_public_key = STRIPE_PUBLIC_KEY
        stripe_secret_key = STRIPE_SECRET_KEY

        booking = request.session.get("booking", {})

        # Bookings are empty
        if not booking:
            messages.error(request, "You have no bookings")
            # This will prevent people from manually accessing the URL
            # by typing "/purchase"
            return redirect(reverse("therapies"))

        # Pass in the request and get the bag dictionary
        current_bookings = booking_contents(request)
        # Retrieve the grand total from the current bag
        total = current_bookings["grand_total"]
        # Stripe requires the amount to charge to be an integer
        stripe_total = total * 100

        stripe.api_key = stripe_secret_key
        # Create the payment intent giving it the amount and the currency
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=STRIPE_CURRENCY,
        )

        # An instance of our order form - which will be empty for now.
        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(
                request,
                "Stripe public key is missing.  Did you forget to set it in your environment?",
            )

        # Context containing the order form.
        context = {
            "order_form": order_form,
            "stripe_public_key": stripe_public_key,
            "client_secret": intent.client_secret,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        bookings = request.session.get("booking", {})

        # Doing this manually in order to skip the save info box,
        # which doesn't have a field on the order model.
        # All the other fields can come directly from the form
        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "street_address1": request.POST["street_address1"],
            "street_address2": request.POST["street_address2"],
            "city": request.POST["city"],
            "county": request.POST["county"],
            "postcode": request.POST["postcode"],
            "country": request.POST["country"],
        }

        # Create an instance of the form using the form data
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # If the form is valid --> save the order.
            # but delay saving to Database until further data
            # which is in the model but not in the OrderForm is collected
            order = order_form.save(commit=False)
            # Split the "client_secret" at the word "_secret"
            # the first part of it will be the payment intent Id
            pid = request.POST.get("client_secret").split("_secret")[0]
            order.stripe_pid = pid
            # Dump the "bookings" to a JSON string and set it on the order
            order.original_booking = json.dumps(bookings)

            order.save()

            # Iterate through the bookings items to create each line item
            # First variable is the key from the bookings item (we call it 'therapy_id')
            # Second variable is the value of that key (we are calling it 'therapy_data')
            for therapy_id, number_of_sessions in bookings.items():
                # For each therapy id and its number of sessions in bookings.items

                try:
                    # First get the therapy.
                    therapy = Therapy.objects.get(id=therapy_id)
                    # For each therapy ordered
                    # Create an order line item and save it
                    order_line_item = OrderLineItem(
                        order=order,
                        therapy=therapy,
                        sessions=number_of_sessions,
                    )
                    order_line_item.save()
                except Therapy.DoesNotExist:
                    messages.error(
                        request,
                        (
                            "One of the therapies you booked was not found in our database.",
                            "Please call us for assistance!",
                        ),
                    )
                    order.delete()
                    return redirect(reverse("bookings"))

            # Attach whether or not the user wanted to save their profile information to the session
            request.session["saveInfo"] = "saveInfo" in request.POST

            # Redirect to a new page
            # passing the order number as an argument
            return redirect(
                reverse("purchaseSuccess", args=[order.order_number])
            )

        else:
            # If the order form isn't valid => attach a message letting the user know
            # and send them back to the purchase page
            # with the form errors shown
            messages.error(
                request,
                "There was an error with your form.  Please double check your information.",
            )

            return render(request, self.template_name, {})


class PurchaseSuccess(TemplateView):
    """
    Handle successful purchases
    """

    template_name = "purchase/purchase-success.html"

    def get(self, request, order_number):
        # first check whether the user wanted to save their information
        # by getting that from the session
        save_info = request.session.get("saveInfo")
        # Use the order number to get the order created in the previous view
        order = get_object_or_404(Order, order_number=order_number)
        print(f"Successful Order  :  {order}")
        # Success message letting the user know what their order number is
        # And that we will be sending an email to the address they put in the form
        messages.success(
            request,
            f"Order successfully processed!  Your order number is\
             <strong>{order_number}</strong>.  A confirmation email will be\
              sent shortly to {order.email}",
            extra_tags="safe",
        )

        # Delete the user's bookings from the session
        # since it'll no longer be needed
        if "booking" in request.session:
            del request.session["booking"]

        context = {"order": order}

        return render(request, self.template_name, context)


class CachePurchaseData(View):
    """
    Determine in the webhook whether the user had the "save info" box checked.
    We can add that to the payment intent in a key called metadata,
    but we have to do it from the server-side
    because the confirm card payment method doesn't support adding it
    """

    # Before we call the confirm card payment method in the stripe JavaScript.
    # we'll make a post request to this view
    # and give it the client secret from the payment intent
    def post(self, request):
        try:
            # Split the "client_secret" at the word "_secret"
            # the first part of it will be the payment intent Id
            pid = request.POST.get("client_secret").split("_secret")[0]
            # Set up stripe with the secret key so we can modify the payment intent
            stripe.api_key = settings.STRIPE_SECRET_KEY
            # Call stripe.PaymentIntent.modify() give it the pid,
            # and tell it what we want to modify.
            # Add some metadata - add the user who's placing the order,
            # add whether or not they wanted to save their information,
            # add a JSON dump of their shopping bag (which we'll use a little later)
            stripe.PaymentIntent.modify(
                pid,
                metadata={
                    "bookings": json.dumps(request.session.get("booking", {})),
                    "save_info": request.POST.get("save_info"),
                    "username": request.user,
                },
            )
            return HttpResponse(status=200)

        except Exception as ex:
            messages.error(
                request,
                "Sorry, your payment cannot be processed right now.  Please try again later.",
            )
            return HttpResponse(content=ex, status=400)
