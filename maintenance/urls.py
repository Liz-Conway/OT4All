from django.urls import path
from maintenance.views import AddTherapy, ListTherapies

urlpatterns = [
    path("add/", AddTherapy.as_view(), name="addTherapy"),
    path("list/", ListTherapies.as_view(), name="listTherapies"),
]
