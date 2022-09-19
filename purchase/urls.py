from django.urls import path
from .views import Purchase

urlpatterns = [
    path("", Purchase.as_view(), name="purchase"),
]
