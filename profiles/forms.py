from django import forms
from profiles.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # Render all fields except for the user field since that should never change
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes,
        and set autofocus on the first field
        """
        # Call the super init() method
        # to set the form up as it would be by default
        super().__init__(*args, **kwargs)
        # A dictionary of placeholders which will show up
        # in the form fields when a default has not been set
        placeholders = {
            "default_full_name": "Your First name and Surname",
            "default_email": "Email address",
            "default_phone_number": "Phone number",
            "default_postcode": "Postal Code",
            "default_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County, State or Locality",
        }

        # Set the "autofocus" attribute on the default_full_namefield to True
        # so the cursor will start in the default_full_name field
        # when the user loads the page
        self.fields["default_full_name"].widget.attrs["autofocus"] = True

        # Iterate through the forms fields
        for field in self.fields:

            if field != "default_country":
                # Set all the placeholder attributes
                # to their values in the dictionary above.
                self.fields[field].widget.attrs["placeholder"] = placeholders[
                    field
                ]

            # Add a CSS class to style each field.
            self.fields[field].widget.attrs["class"] = "formInput"
