from django import forms
from .models import Testimonial
from maintenance.widgets import CustomClearableFileInput


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial

        # Special dunder string called __all__
        # which will include all the fields
        fields = "__all__"

        # Replace the image field on the form
        # with the custom one which utilises the widget
        image = forms.ImageField(
            label="Image", required=False, widget=CustomClearableFileInput
        )
