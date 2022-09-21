from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.template import context


class ProfileView(TemplateView):
    """
    Display the user's profile
    """

    template_name = "profiles/profile.html"

    def get_context_data(self, request, *args, **kwargs):
        context = {}

        return context
