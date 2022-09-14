from django.urls import path
from home.views import HomePage, MeejaPage, MeejaPage2

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("meeja/", MeejaPage.as_view(), name="meeja"),
    path("meeja2/", MeejaPage2.as_view(), name="meeja2"),
]
