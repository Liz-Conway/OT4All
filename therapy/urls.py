from django.urls import path
from .views import AllTherapies, SingleTherapy

# from maintenance.views import  AddTherapy, ListTherapies

urlpatterns = [
    path("", AllTherapies.as_view(), name="therapies"),
    path("<int:therapy_id>/", SingleTherapy.as_view(), name="singleTherapy"),
    # path("add/", AddTherapy.as_view(), name="addTherapy"),
    # path("list/", ListTherapies.as_view(), name="listTherapies"),
]
