import uuid  # used to generate the order number
from django.db import models
from django.db.models import Sum
from therapy.models import Therapy


class Order(models.Model):

    # "editable=False" attribute on the order number field.
    # We're gonna automatically generate this order number.
    # And we'll want it to be unique and permanent
    # so users can find their previous orders.
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
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
        max_digits=10, decimal_places=2, null=False, default=0
    )

    # Prepended with an underscore by convention
    # to indicate it's a private method
    # which will only be used inside this class
    def _generate_order_number(self):
        """
        Generate a random, unique number using UUID
        """
        # Generate a random string of 32 characters
        # we can use as an order number
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        # Use the Sum() function across all the line-item total fields
        # for all line items on this order.
        # Use the aggregate() function
        # to add a new field to the query set called "lineitem_total_sum"
        # this field is named automatically for us.
        # We can then get the "lineitem_sum" and set the grand total to it.
        self.grand_total = self.lineitems.aggregate(Sum("lineitem_total"))[
            "lineitem_total_sum"
        ]

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
            along with the order number it's part of for each order line item
            """
            return (
                f"Therapy {self.therapy.name}"
                f" on order {self.order.order_number}"
            )
