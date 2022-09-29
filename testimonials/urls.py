from django.urls import path
from .views import Testimonials, AddTestimonial

urlpatterns = [
    path("", Testimonials.as_view(), name="testimonials"),
    path("add/", AddTestimonial.as_view(), name="addTestimonial"),
]
