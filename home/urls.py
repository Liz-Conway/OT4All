from django.urls import path
from home.views import HomePage, MeejaPage

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("meeja/", MeejaPage.as_view(), name="meeja"),
]
