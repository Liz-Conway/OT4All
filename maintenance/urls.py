from django.urls import path
from maintenance.views import (
    AddTherapy,
    ListTherapies,
    EditTherapy,
    DeleteTherapy,
)

urlpatterns = [
    path("add/", AddTherapy.as_view(), name="addTherapy"),
    path("list/", ListTherapies.as_view(), name="listTherapies"),
    path("edit/<int:therapy_id>/", EditTherapy.as_view(), name="editTherapy"),
    path(
        "delete/<int:therapy_id>/",
        DeleteTherapy.as_view(),
        name="deleteTherapy",
    ),
]
