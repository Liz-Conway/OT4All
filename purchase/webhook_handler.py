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
import therapy
from therapy.models import Therapy
import json
import time


class StripeWH_Handler:
    """Handle Stripe WebHooks"""

    # A setup method that's called every time an instance of the class is created
    def __init__(self, request):
        # Assign the request as an attribute of the class
        # just in case we need to access any attributes of the request coming from stripe
        self.request = request

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

        # Most of the time when a user checks out,
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
            # Which was created with the exact same shopping bag.
            # And is associated with the same payment intent.

            # To remove all doubt as to which order we're looking for,
            # here in the webhook handler;
            # Add the bookings and the stripe pid
            # to the list of attributes we want to match on when finding the order
            try:
                # Get the order using all the information from the payment intent
                order = Order.objects.get(
                    # Using the "iexact" lookup field to make it an exact match but case-insensitive
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
                    # Add thebookings and the stripe pid
                    # to the list of attributes we want to match on when finding the order
                    original_booking=bookings,
                    stripe_pid=pid,
                )
                # If the order exists - set "order_exists" to True
                order_exists = True
                # If the order exists then break out of the loop
                break

            except Order.DoesNotExist:
                print("Exception Order.DoesNotExist")
                attempts += 1
                # Use python's time module to sleep for one second
                time.sleep(1)

        if order_exists:
            print("This order already exists")
            # STEP 3a
            # When we find the existing order
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
                # We don't have a form to save in this webhook to create the order
                # but we can do it just as easily with Order.objects.create()
                # using all the data from the payment intent.
                # After all, it came from the form originally anyway
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
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
                # Iterate through the bag items to create each line item
                # Load the bag from the JSON version in the PaymentIntent
                # instead of from the session
                # First variable is the key from the bag item (we call it 'therapy_id')
                # Second variable is the value of that key (we are calling it 'number_of_sessions')
                for therapy_id, number_of_sessions in json.loads(
                    bookings
                ).items():
                    # For each therapy id and number of sessions in bookings.items
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
                # This will cause stripe to automatically try the webhook again later.
                if order:
                    order.delete()

                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {ex}',
                    status=500,
                )

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
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
