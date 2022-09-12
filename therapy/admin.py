from django.contrib import admin
from .models import Therapy, Style


class TherapyAdmin(admin.ModelAdmin):
    # list display attribute
    # - a tuple that will tell the admin which fields to display.
    list_display = (
        "style",
        "name",
        "price",
        "image",
    )

    # Sort the products by Style and Name using the ordering attribute.
    # Since it's possible to sort on multiple columns note that this does
    # have to be a tuple even when it's only one field.
    # To reverse it you can simply stick a minus in front of the field name.
    # I.E. '-style'
    ordering = ("style", "name")


class StyleAdmin(admin.ModelAdmin):
    list_display = ("name",)


# Register the *Admin classes alongside their respective models
admin.site.register(Therapy, TherapyAdmin)
admin.site.register(Style, StyleAdmin)
