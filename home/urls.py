from django.urls import path
from home.views import HomePage, ContactView, AboutPage

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("contact/", ContactView.as_view(), name="getInTouch"),
    path("about/", AboutPage.as_view(), name="about"),
]
