from django import forms
from purchase.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        # Notice that we're not rendering any fields in the form
        # which will be automatically calculated.
        # Since no one will ever be filling that information out.
        # It'll all be done via the model methods we've created.
        fields = [
            "full_name",
            "email",
            "phone_number",
            "street_address1",
            "street_address2",
            "city",
            "county",
            "postcode",
            "country",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "formInput", "placeholder": "Full name*"}
            ),
            "email": forms.TextInput(
                attrs={"class": "formInput", "placeholder": "Email Address*"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "formInput", "placeholder": "Phone Number*"}
            ),
            "street_address1": forms.TextInput(
                attrs={
                    "class": "formInput",
                    "placeholder": "Street Address 1*",
                }
            ),
            "street_address2": forms.TextInput(
                attrs={"class": "formInput", "placeholder": "Street Address 2"}
            ),
            "city": forms.TextInput(
                attrs={"class": "formInput", "placeholder": "City*"}
            ),
            "county": forms.TextInput(
                attrs={"class": "formInput", "placeholder": "County*"}
            ),
            # "country": forms.TextInput(
            #     attrs={"class": "formInput", "placeholder": "Country*"}
            # ),
            "postcode": forms.TextInput(
                attrs={"class": "formInput", "placeholder": "Post Code*"}
            ),
        }

        def __init__(self, *args, **kwargs):
            """
            Add placeholders and classes, remove auto-generated
            labels and set autofocus on the first field
            """
            # Call the super init() method
            # to set the form up as it would be by default
            super().__init__(*args, *kwargs)

            # Set the "autofocus" attribute on the full_name field to True
            # so the cursor will start in the full_name field
            # when the user loads the page
            self.fields["full_name"].widget.attrs["autofocus"] = True
            # Iterate through the forms fields
            for field in self.fields:
                # Add a CSS class to use for the Stripe input.
                self.fields[field].widget.attrs["class"] = "stripeStyleInput"
                # Remove the form fields' labels
                # since we won't need them given the placeholders are set
                self.fields[field].label = False
