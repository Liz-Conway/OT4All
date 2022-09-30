"""
If the user somehow intentionally or accidentally
closes the browser window after the payment
is confirmed but before the form is submitted.
We would end up with a payment in stripe
but no order in our database.
What's more, if we needed to complete
post order operations like fulfillment,
sending internal email notifications and so on;
none of that stuff would be triggered
because the user never fully completed their order.
This could result in a customer being charged
and never receiving a confirmation email
or even worse never receiving what they ordered.
To prevent this situation we're going to build in some redundancy.
Each time an event occurs on stripe such as a payment intent being created,
a payment being completed, and so on;
stripe sends out what's called a webhook we can listen for.
Webhooks are like the signals
django sends each time a model is saved or deleted.
Except that they're sent securely from stripe to a URL we specify.
"""
from django.http.response import HttpResponse
from purchase.models import OrderLineItem, Order
from therapy.models import Therapy
import json
import time
from profiles.models import UserProfile
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail


class StripeWH_Handler:
    """Handle Stripe WebHooks"""

    # A setup method that's called
    # every time an instance of the class is created
    def __init__(self, request):
        # Assign the request as an attribute of the class
        # just in case we need to access any attributes
        # of the request coming from stripe
        self.request = request

    # Prepended with an underscore by convention
    # to indicate it's a private method
    # which will only be used inside this class
    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        # The best place to do this is the webhook handler
        # since at that point we know the payment has definitely been made.
        # Since the only thing that can trigger it is a webhook from Stripe.
        cust_email = order.email

        # Use the render_to_string() method to render
        # both the confirmation text files as two strings.
        # With the first parameter being the file we want to render.
        # And the second being a context
        # just like we would pass to a template.
        # This is how we'll be able to render the
        # various context variables in the confirmation email.
        subject = render_to_string(
            "purchase/confirmation-emails/confirmation-email-subject.txt",
            {"order": order},
        )
        body = render_to_string(
            "purchase/confirmation-emails/confirmation-email-body.txt",
            {"order": order, "contact_email": settings.DEFAULT_FROM_EMAIL},
        )

        # Giving it the subject, the body,
        # the email address we want to send from.
        # and a list of emails we're sending to -
        # which in this case will be only the customer's email
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])

    # Take the event stripe is sending us
    # and simply return an HTTP response indicating it was received.
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200
        )

    # Sent each time a user completes the payment process
    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        # STEP 1
        # When we receive a webhook from stripe
        # that a payment has been processed successfully.

        # Once the user makes a payment, it will have our metadata attached.
        # The payment intent will be saved in a key called "event.data.object"
        intent = event.data.object

        pid = intent.Id
        bookings = intent.metadata.bookings
        save_info = intent.metadata.saveInfo

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = intent.charges.data[0].amount / 100

        # Clean data in the shipping details
        # To ensure the data is in the same form
        # as what we want in our database
        # Replace any empty strings in the shipping details with "None".
        # Since stripe will store them as blank strings
        # which is not the same as the "null" value we want in the database.
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # If the purchase view fails
        # we can depend on the webhook handler to handle the user profiles.
        # Update profile information if set_info was checked
        profile = None
        #  Still allow anonymous users to checkout
        username = intent.metadata.username
        if username != "AnonymousUser":
            # If the username isn't "AnonymousUser"
            # => they were authenticated.
            # We could also use request.user here,
            # since we added the request object in the init method above.

            # Get the user's profile using their username.
            profile = UserProfile.objects.get(user__username=username)
            # If they've got the save info box checked
            # (from the metadata we added).
            if save_info:
                # Update their profile by adding the shipping & billing details
                # as their default client information.
                profile.default_full_name = (shipping_details.name,)
                profile.default_email = (billing_details.email,)
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = billing_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = (
                    shipping_details.address.line1
                )
                profile.default_street_address2 = (
                    shipping_details.address.line2
                )
                profile.default_county = shipping_details.address.state

                profile.save()

        # Most of the time when a client checks out,
        # everything will go well and the form will be submitted
        # so the order should already be in our database
        # when we receive this webhook.
        # The first thing then is to check if the order exists already.
        # If it does just return a response, and say everything is all set.
        # And if it doesn't we'll create it here in the webhook.
        order_exists = False
        # What if our view is just slow for some reason
        # and hasn't created the order
        # by the time we get the webhook from stripe.
        # In that case, perhaps everything is fine in the view
        # and it'll create the order but it might be a few seconds late.
        # This is not good because our webhook handler won't find the order
        # when it first gets the webhook from stripe
        # and will create the order itself resulting in the
        # same order being added to the database twice,
        # once the view finally finishes.
        attempts = 1
        # Check if the order is in the database up to 5 times
        while attempts <= 5:
            # STEP 2
            # We'll try to find an order with the same
            # customer information and the same grand total,
            # Which was created with the exact same bookings.
            # And is associated with the same payment intent.

            # To remove all doubt as to which order we're looking for,
            # here in the webhook handler;
            # Add the bookings and the stripe pid
            # to the list of attributes we want to match on
            # when finding the order
            try:
                # Get the order using all the information
                # from the payment intent
                order = Order.objects.get(
                    # Using the "iexact" lookup field
                    # to make it an exact match but case-insensitive
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=billing_details.address.postal_code,
                    city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    # To remove all doubt as to which order we're looking for,
                    # here in the webhook handler;
                    # Add the bookings and the stripe pid
                    # to the list of attributes we want to match on
                    # when finding the order
                    original_booking=bookings,
                    stripe_pid=pid,
                )
                # If the order exists - set "order_exists" to True
                order_exists = True
                # If the order exists then break out of the loop
                break

            except Order.DoesNotExist:
                attempts += 1
                # Use python's time module to sleep for one second
                time.sleep(1)

        if order_exists:
            # STEP 3a
            # When we find the existing order

            # Since in the webhook payment_succeeded handler,
            # the payment has definitely been completed at this point.
            # Found the order in the database
            # because it was already created by the form.
            # Send the confirmation email
            # just before returning the response to Stripe
            self._send_confirmation_email(order)

            # Return a 200 response
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS\
                : Verified order already in database',
                status=200,
            )
        else:
            # STEP 3b
            # If there is no matching order on the database
            # Create an order with the details from the form
            order = None
            try:
                # We don't have a form to save in this webhook
                # to create the order
                # but we can do it just as easily with Order.objects.create()
                # using all the data from the payment intent.
                # After all, it came from the form originally anyway
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    # Set the user's profile,
                    # if they weren't logged in it will just be None.
                    # Add their profile to their order
                    # when the webhook creates it.
                    # In this way, the webhook handler can create orders
                    # for both authenticated users by attaching their profile.
                    # and for anonymous users
                    # by setting the user_profile field to None.
                    user_profile=profile,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    grand_total=grand_total,
                    original_booking=bookings,
                    stripe_pid=pid,
                )
                # Iterate through the bookings items to create each line item
                # Load the bookings from the JSON version in the PaymentIntent
                # instead of from the session
                # First variable is the key from the
                # bookings item (we call it 'therapy_id')
                # Second variable is the value of that
                # key (we are calling it 'number_of_sessions')
                for therapy_id, number_of_sessions in json.loads(
                    bookings
                ).items():
                    # For each therapy id and
                    # number of sessions in bookings.items
                    # First get the therapy
                    therapy = Therapy.objects.get(id=therapy_id)
                    # For each therapy ordered
                    # Create an order line item and save it
                    order_line_item = OrderLineItem(
                        order=order,
                        therapy=therapy,
                        sessions=number_of_sessions,
                    )
                    order_line_item.save()
            except Exception as ex:
                # If anything goes wrong - delete the order if it was created.
                # And return a 500 server error response to stripe.
                # This will cause stripe to automatically
                # try the webhook again later.
                if order:
                    order.delete()

                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {ex}',
                    status=500,
                )

        # Since in the webhook payment_succeeded handler,
        # the payment has definitely been completed at this point.
        # If the order was created by the webhook handler
        # Send the confirmation email
        # just before returning the response to Stripe
        self._send_confirmation_email(order)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | \
            SUCCESS: Created order in webhook',
            status=200,
        )

    # Sent when the payment fails
    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200
        )
