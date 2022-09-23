from django import forms
from therapy.models import Therapy, Style
from therapy.widgets import CustomClearableFileInput


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
        super().__init__(*args, **kwargs)
        # Get all styles
        styles = Style.objects.all()

        # iterate through the rest of these fields
        for field_name, field in self.fields.items():
            # Set some classes on them to make them match the theme of the rest of our store
            field.widget.attrs["class"] = "formInput"
