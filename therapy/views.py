from django.views.generic.base import TemplateView
from therapy.models import Therapy
from django.shortcuts import render, get_object_or_404
from django.db.models.functions.text import Lower


# Create your views here.
class AllTherapies(TemplateView):
    """A class for rendering a page containing all available therapies"""

    template_name = "therapy/therapies.html"

    # TemplateView does not need to define get() method
    # But here we need to tell the page what Therapies to show so we will
    def get(self, request, *args, **kwargs):
        all_therapies = Therapy.objects.all()

        # Start as none to ensure we don't get an error
        # when loading the products page without a search term.
        query = None
        sort = None
        direction = None

        # Access URL parameters by checking whether request.GET exists
        if request.GET:
            if "sort" in request.GET:
                sortkey = request.GET["sort"]
                sort = sortkey
                if sortkey == "name":
                    # annotate() allows us to add another field to the
                    # dataset returned from the database.
                    # Using the Lower() function on the original "name" field
                    all_therapies = all_therapies.annotate(
                        lower_name=Lower("name")
                    )
                    # The reason for copying the sort parameter
                    # into a new variable called sortkey,
                    # Is because now we've preserved the original field
                    # we want to sort on ("name").
                    # But we have the actual field we're going to sort on,
                    # ("lower_name") in the sort key variable.
                    # If we had just renamed sort itself to "lower_name"
                    # we would have lost the original field ("name")

                    # set the sortKey to lower_name
                    sortkey = "lower_name"

                if sortkey == "category":
                    sortkey = "category__name"

                if "direction" in request.GET:
                    direction = request.GET["direction"]
                    if direction == "desc":
                        # Add a minus in front of the sort key
                        # using string formatting, which reverses the order
                        sortkey = f"-{sortkey}"

                all_therapies = all_therapies.order_by(sortkey)

        # If there is no sorting
        # The value of this variable will be the string "None_None".
        current_sorting = f"{sort}_{direction}"

        context = {
            "therapies": all_therapies,
            "current_sorting": current_sorting,
        }

        return render(request, self.template_name, context)


class SingleTherapy(TemplateView):
    """
    A view to show all details for an individual therapy
    """

    template_name = "therapy/therapy-details.html"

    def get(self, request, therapy_id):
        single_therapy = get_object_or_404(Therapy, pk=therapy_id)

        context = {
            "therapy": single_therapy,
        }

        return render(request, self.template_name, context)
