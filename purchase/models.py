from django.db import models
from django.db.models import Sum
from therapy.models import Therapy
from django.db.models.aggregates import Max
from django_countries.fields import CountryField
from profiles.models import UserProfile


class Order(models.Model):

    # "editable=False" attribute on the order number field.
    # We're gonna automatically generate this order number.
    # And we'll want it to be unique and permanent
    # so users can find their previous orders.
    order_number = models.CharField(max_length=32, null=False, editable=False)
    #  Foreign key to "userprofile" on the order.
    # Use models.SET_NULL
    # if the profile is deleted since that will allow us to keep
    # an order history in the admin even if the user is deleted.
    # Allow this to be either "null" or "blank"
    # UNTIL we force clients to login to make a booking.
    # Add a related name of "orders" so we can access
    # the user's orders by calling something like user.userprofile.orders
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    # blank_label -
    # use "Country" with the star to indicate it's a required field
    # since select boxes don't have a placeholder
    country = CountryField(blank_label="Country *", null=False, blank=False)
    # The postcode field is used to compare orders
    # So it cannot be blank on the form
    postcode = models.CharField(max_length=20, null=False, blank=False)
    city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    # Use "auto_now_add" attribute on the date field
    # which will automatically set the order date and time
    # whenever a new order is created
    date = models.DateField(auto_now_add=True)

    # The last field will be calculated using a model method.
    # whenever an order is saved
    grand_total = models.DecimalField(
        max_digits=5, decimal_places=0, null=False, default=0
    )

    # It's possible for the same customer to purchase
    # the same things twice on separate occasions
    # which would result in us finding an identical order in the database
    # when they place the second one.
    # These field ensure that each order is unique
    original_bookings = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default=""
    )

    # Prepended with an underscore by convention
    # to indicate it's a private method
    # which will only be used inside this class
    def _generate_order_number(self):
        """
        Generate a random, unique number based on
        the max id in the database
        """
        max_id = Order.objects.aggregate(Max("id"))
        last_id = max_id.get("id__max")
        # If this is the first order
        # there will not be any max id in the database
        # Instead it will return 'None'
        # Convert this to 0 (zero)
        if not last_id:
            last_id = 0

        new_order = str(last_id + 1)
        return new_order.zfill(8)

    def update_total(self):
        """
        Update grand total each time a line item is added
        """
        # Use the Sum() function across all the line-item total fields
        # for all line items on this order.
        # Use the aggregate() function
        # to add a new field to the query set called "lineitem_total_sum"
        # this field is named automatically for us.
        # We can then get the "lineitem_sum" and set the grand total to it.
        # NB THERE IS A DOUBLE UNDERSCORE  BEFORE 'sum' where it is aggregated
        aggregation = self.lineitems.aggregate(Sum("lineitem_total"))
        line_sum = aggregation["lineitem_total__sum"]
        # Add " or 0" to the end to prevent an error
        # if we manually delete all the line items from an order
        # by making sure that this sets the order_total to zero instead of None
        self.grand_total = line_sum or 0

        self.save()

    # Override the default save method.
    # If the order we're saving right now doesn't have an order number.
    # We'll call the generate_order_number() method.
    # And then execute the original save() method
    def save(self, *args, **kwargs):
        """
        Override the original save() method to set the order number
        if it hasn't been set already
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()

        super().save(*args, **kwargs)

        def __str__(self):
            """
            Return the order number
            """
            return self.order_number


class OrderLineItem(models.Model):
    """
    An individual booking item relating to a specific order
    And referencing the therapy itself,
    the number of sessions and the total cost for that line item.
    When a user checks out:
    First use the information they put into the payment form
    to create an order instance.
    Iterate through the items in the bookings.
    Create an order line item for each therapy, attaching it to the order.
    Update the grand total along the way.
    """

    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="lineitems",
    )
    therapy = models.ForeignKey(
        Therapy,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    sessions = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=5,
        decimal_places=0,
        null=False,
        blank=False,
        # Automatically calculated when the line item is saved
        editable=False,
    )

    # Override the default save method.
    # And then execute the original save() method
    def save(self, *args, **kwargs):
        """
        Override the original save() method to set the lineitem total
        and update the order total
        """
        # Multiply the therapy price by the sessions for each line item
        self.lineitem_total = self.therapy.price * self.sessions

        super().save(*args, **kwargs)

        def __str__(self):
            """
            Return the Therapy name
            along with the order number it's part of, for each order line item
            """
            return (
                f"Therapy {self.therapy.name}"
                f" on order {self.order.order_number}"
            )
