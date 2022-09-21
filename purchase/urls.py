from django.urls import path
from .views import Purchase, PurchaseSuccess, CachePurchaseData

# The webhook() function will live in a file called "webhooks.py"
from .webhooks import webhook

urlpatterns = [
    path("", Purchase.as_view(), name="purchase"),
    path(
        "purchase-success/<order_number>",
        PurchaseSuccess.as_view(),
        name="purchaseSuccess",
    ),
    path(
        "cachePurchaseData/",
        CachePurchaseData.as_view(),
        name="cachePurchaseData",
    ),
    path("wh/", webhook, name="webhook"),
]
# Path "wh/" will return a function called "webhook()" with the name of "webhook"
