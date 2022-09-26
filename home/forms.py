from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact

        # Special dunder string called __all__
        # which will include all the fields
        fields = "__all__"
