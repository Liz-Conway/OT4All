from django.urls import path
from .views import Purchase, PurchaseSuccess

urlpatterns = [
    path("", Purchase.as_view(), name="purchase"),
    path(
        "purchase-success/<order_number>",
        PurchaseSuccess.as_view(),
        name="purchaseSuccess",
    ),
]
