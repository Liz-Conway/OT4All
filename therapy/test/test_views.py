"""
@author: liz
"""
from django.test import TestCase, Client
from therapy.models import Therapy, Style
from django.urls.base import reverse
from datetime import datetime
from django.contrib.messages.api import get_messages


class TherapyViewsTest(TestCase):
    def setUp(self):
        self.style = Style.objects.create(name="Test Style")
        self.therapy = Therapy.objects.create(
            name="Test Therapy",
            description="A test therapy for use in unit testing",
            price=100,
            course_sessions=3,
            style=self.style,
        )

        self.optional_therapy = Therapy.objects.create(
            name="Test Therapy optional fields",
            description="A test therapy for use in unit testing.  Some optional fields are included",
            price=200,
            course_sessions=6,
            style=self.style,
            location="My gymnasium",
            extra_requirements="Hard work, elbow grease and a fun attitude",
        )

        self.therapies_url = reverse("therapies")
        self.book_therapy_url = reverse(
            "singleTherapy", args=[self.therapy.id]
        )
        self.list_therapies_url = reverse("listTherapies")
        self.add_therapy_url = reverse("addTherapy")

    def test_show_therapies_page(self):
        response = self.client.get(self.therapies_url)

        self.assertEqual(
            response.status_code,
            200,
            "Going to 'Our Therapies' page should return a Status Code of 200 (OK)",
        )
        self.assertTemplateUsed(
            response,
            "therapy/therapies.html",
            "Therapies page should use the therapies.html template",
        )

    def test_show_single_therapy_page(self):
        response = self.client.get(self.book_therapy_url)

        self.assertEqual(
            response.status_code,
            200,
            "Going to 'Book Therapy' page should return a Status Code of 200 (OK)",
        )
        self.assertTemplateUsed(
            response,
            "therapy/therapy-details.html",
            "Book Therapy page should use the therapy-detail.html template",
        )

    def test_show_therapies_list(self):
        response = self.client.get(self.list_therapies_url)

        self.assertEqual(
            response.status_code,
            200,
            "Going to 'Therapies List' page should return a Status Code of 200 (OK)",
        )
        self.assertTemplateUsed(
            response,
            "therapy/list-therapies.html",
            "List Therapies page should use the list-therapies.html template",
        )

    def test_show_add_therapies_page(self):
        response = self.client.get(self.add_therapy_url)

        self.assertEqual(
            response.status_code,
            200,
            "Going to 'Add Therapy' page should return a Status Code of 200 (OK)",
        )
        self.assertTemplateUsed(
            response,
            "therapy/add-therapy.html",
            "Add Therapy page should use the add-therapy.html template",
        )

    def test_post_add_therapy(self):
        therapy_data = {
            "name": "Test Therapy",
            "description": "A test therapy for use in unit testing",
            "price": 100,
            "course_sessions": 3,
            "style": self.style.id,
        }

        response = self.client.post(self.add_therapy_url, therapy_data)
        # messages = list(response.context['messages'])

        self.assertEqual(
            response.status_code,
            302,
            "Posting the Add Therapy form should\
             return a Status Code of 302 (OK)",
        )

        self.compare_therapies(Therapy.objects.last(), self.therapy)

    def test_post_add_therapy_optional_fields(self):
        therapy_data = {
            "name": "Test Therapy optional fields",
            "description": "A test therapy for use in unit testing.  Some optional fields are included",
            "price": 200,
            "course_sessions": 6,
            "style": self.style.id,
            "location": "My gymnasium",
            "extra_requirements": "Hard work, elbow grease and a fun attitude",
        }

        response = self.client.post(self.add_therapy_url, therapy_data)
        # messages = list(response.context['messages'])

        self.assertEqual(
            response.status_code,
            302,
            "Posting the Add Therapy form should\
             return a Status Code of 302 (OK)",
        )

        self.compare_therapies(Therapy.objects.last(), self.optional_therapy)

    def compare_therapies(self, therapy_one, therapy_two):
        self.assertEqual(
            therapy_one.name, therapy_two.name, "Therapy names should be equal"
        )
        self.assertEqual(
            therapy_one.description,
            therapy_two.description,
            "Therapy descriptions should be equal",
        )
        self.assertEqual(
            therapy_one.style,
            therapy_two.style,
            "Therapy styles should be equal",
        )
        self.assertEqual(
            therapy_one.price,
            therapy_two.price,
            "Therapy prices should be equal",
        )
        self.compare_image_fields(therapy_one.image, therapy_two.image)
        self.assertEqual(
            therapy_one.course_sessions,
            therapy_two.course_sessions,
            "Therapy course sessions should be equal",
        )
        self.assertEqual(
            therapy_one.location,
            therapy_two.location,
            "Therapy locations should be equal",
        )
        self.compare_text_fields(
            therapy_one.extra_requirements,
            therapy_two.extra_requirements,
            "Therapy extra requirements should be equal",
        )

    def compare_image_fields(self, image_field1, image_field2):
        if image_field1 == None or image_field1 == "":
            if image_field2 == None or image_field2 == "":
                # Both are blank so test passes
                return

        self.assertEqual(
            image_field1, image_field2, "Therapy images should be equal"
        )

    def compare_text_fields(self, text_field1, text_field2, field_name):
        if text_field1 == None or text_field1 == "":
            if text_field2 == None or text_field2 == "":
                # Both are blank so test passes
                return

        self.assertEqual(
            text_field1, text_field2, f"{field_name} texts should be equal"
        )
