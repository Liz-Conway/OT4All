from django import forms
from purchase.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Notice that we're not rendering any fields in the form
        # which will be automatically calculated.
        # Since no one will ever be filling that information out.
        # It'll all be done via the model methods we've created.
        fields = (
            "full_name",
            "email",
            "phone_number",
            "street_address1",
            "street_address2",
            "city",
            "postcode",
            "country",
            "county",
        )

        def __init__(self, *args, **kwargs):
            """
            Add placeholders and classes, remove auto-generated
            labels and set autofocus on the first field
            """
            # Call the super init() method
            # to set the form up as it would be by default
            super().__init__(*args, *kwargs)
            # A dictionary of placeholders which will show up
            # in the form fields rather than having
            # clunky looking labels and empty text boxes.
            placeholders = {
                "full_name": "Full name",
                "email": "Email Address",
                "phone_number": "Phone number",
                "country": "Country",
                "postcode": "Postal Code",
                "city": "Town or City",
                "street_address1": "Street Address 1",
                "street_address2": "Street Address 2",
                "county": "County",
            }

            # Set the "autofocus" attribute on the full_name field to True
            # so the cursor will start in the full_name field
            # when the user loads the page
            self.fields["full_name"].widget.attrs["autofocus"] = True
            # Iterate through the forms fields
            for field in self.fields:
                if self.fields[field].required:
                    # Add a star to the placeholder
                    # if it's a "required" field on the model.
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholder[field]

                # Set all the placeholder attributes
                # to their values in the dictionary above.
                self.fields[field].widget.attrs["placeholder"] = placeholder
                # Add a CSS class we'll use for the Stripe input.
                self.fields[field].widget.attrs["class"] = "stripeStyleInput"
                # Remove the form fields' labels
                # since we won't need them given the placeholders are now set
                self.fields[field].label = False
