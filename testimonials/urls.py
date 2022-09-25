from django.urls import path
from .views import Testimonials

urlpatterns = [
    path("", Testimonials.as_view(), name="testimonials"),
]
