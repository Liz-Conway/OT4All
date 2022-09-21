from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.template import context
from profiles.models import UserProfile


class ProfileView(TemplateView):
    """
    Display the user's profile
    """

    template_name = "profiles/profile.html"

    def get_context_data(self, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=self.request.user)
        # Call the base implementation first to get a context
        context = super().get_context_data(*args, **kwargs)
        context["profile"] = profile

        return context
