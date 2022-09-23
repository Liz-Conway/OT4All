# Default config class for the app
# Without this line, django wouldn't know about our
# custom ready method so our signals wouldn't work.
default_app_config = "purchase.apps.PurchaseConfig"
