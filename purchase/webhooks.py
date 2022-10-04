import stripe
from django.http.response import HttpResponse
from django.conf import settings
from .webhook_handler import StripeWH_Handler

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


# Will make this view require a post request and will reject get requests
@require_POST
# Stripe won't send a CSRF token like we'd normally use
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, wh_secret)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)
    # Generic exception handler
    except Exception as ex:
        return HttpResponse(content=ex, status=400)

    # Set up a webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler function
    # Dictionary keys => names of the webhooks coming from stripe.
    # Values => the actual methods inside the handler.
    event_map = {
        "payment_intent.succeeded": handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed":
            handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from Stripe
    # which will be stored in a key called "type"
    # E.G.  "payment_intent.succeeded" or "payment_intent.payment failed"
    event_type = event["type"]

    # Look up the key in the dictionary.
    # And assign its value to a variable called "event_handler"
    # If there is a handler for it, get it from the event map
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    response = event_handler(event)

    return response
