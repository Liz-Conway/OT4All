from django.views.generic.edit import FormView
from django.urls.base import reverse_lazy
from .forms import ContactForm
from django.views.generic.base import TemplateView


class ContactView(FormView):
    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contactSuccess")

    def form_valid(self, form):
        # Calls the custom send method
        form.send()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = "contact/contactSuccess.html"
