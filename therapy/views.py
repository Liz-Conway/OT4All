from django.views.generic.base import TemplateView
from therapy.models import Therapy, Style
from django.shortcuts import render, get_object_or_404
from django.db.models.functions.text import Lower
from pip._vendor.pygments import styles


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
        style = None
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

                therapies = all_therapies.order_by(sortkey)

            # Filter the therapies by the style chosen by the client
            if "style" in request.GET:
                # Split it into a list at the commas.
                styles = request.GET["style"].split(",")
                # Use that list to filter the current query set of all therapies
                # down to only therapies whose style name is in the list
                filter_therapies = all_therapies.filter(style__name__in=styles)
                # Filter a list of Style objects
                # to those passed in the URL parameter
                style = Style.objects.filter(name__in=styles)

                therapies = filter_therapies

        else:
            # If there are no GET parameters, return ALL therapies
            therapies = all_therapies

        all_styles = Style.objects.all()

        # If there is no sorting
        # The value of this variable will be the string "None_None".
        current_sorting = f"{sort}_{direction}"

        context = {
            "therapies": therapies,
            "current_sorting": current_sorting,
            "chosen_styles": style,
            "all_styles": all_styles,
        }

        print(f"Chosen Styles :  {style}")
        print(f"All Styles :  {all_styles}")

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
