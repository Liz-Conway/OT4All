from django import forms
from therapy.models import Therapy, Style
from .widgets import CustomClearableFileInput


class TherapyForm(forms.ModelForm):
    class Meta:
        model = Therapy

        # Special dunder string called __all__ which will include all the fields
        fields = "__all__"

        # Replace the image field on the form with the custom one which utilises the widget
        image = forms.ImageField(
            label="Image", required=False, widget=CustomClearableFileInput
        )
        # Override the __init__ method to make a couple changes to the fields
        def __init__(self, *args, **kwargs):
            """
            Add placeholders and classes, remove auto-generated
            labels and set autofocus on the first field
            """
            # Call the super init() method
            # to set the form up as it would be by default
            super().__init__(*args, *kwargs)
            # A dictionary of placeholders which will show up
            # in the form fields rather than having empty text boxes.
            placeholders = {
                "style": "No placeholder needed",
                "name": "Therapy name",
                "description": "Description of Therapy",
                "price": "Price in €",
                "image": "No placeholder needed",
                "course_sessions": "Default amount of sessions",
                "location": "Where takes place (if any)",
                "extra_requirements": "Any additional requirements this therapy will need",
            }
            print(f"Placeholders :  {placeholders}")

            try:
                # Set the "autofocus" attribute on the name field to True
                # so the cursor will start in the name field
                # when the client loads the page
                self.fields["name"].widget.attrs["autofocus"] = True
                print(f"Autofocus done")
                # Iterate through the forms fields
                for field in self.fields:
                    print(f"Field :  {field}")
                    if self.fields[field].required and field != "style":
                        print(f"Gold star")
                        # Add a star to the placeholder
                        # if it's a "required" field on the model.
                        placeholder = f"{placeholders[field]} *"
                        print("Placeholder")
                    else:
                        placeholder = placeholders[field]

                    # Set all the placeholder attributes
                    # to their values in the dictionary above.
                    if field != "style":
                        if field != "image":
                            self.fields[field].widget.attrs[
                                "placeholder"
                            ] = placeholder
                            print(f"{field} placeholder set")
                    self.fields[field].widget.attrs["class"] = "formInput"
                    print(f"{field} class set")
            except Exception as ex:
                print(f"Error :  {ex.message}")
