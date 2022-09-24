from django.test import TestCase
from therapy.models import Therapy, Style
from django.core.files.uploadedfile import SimpleUploadedFile


class TherapyTest(TestCase):
    def setUp(self):
        self.style = Style.objects.create(name="Test Style")
        self.style_equipped = Style.objects.create(
            name="Equipped Style",
            equipment="List of any equipment required by this particular style",
        )
        self.therapy = Therapy.objects.create(
            name="Test Therapy",
            description="A test therapy for use in unit testing",
            price=100,
            course_sessions=3,
            style=self.style,
        )

        self.full_therapy = Therapy.objects.create(
            name="Full Therapy",
            description="A test therapy for use in unit testing.  Has optional text fields filled.",
            price=100,
            course_sessions=3,
            style=self.style_equipped,
            location="My therapeutic offices",
            extra_requirements="A list of extra requirements needed",
        )

    def test_therapy_string(self):
        self.assertEqual(self.therapy.__str__(), "Test Therapy")

    def test_full_therapy_string(self):
        self.assertEqual(self.full_therapy.__str__(), "Full Therapy")

    def test_therapy_style(self):
        self.assertEqual(self.therapy.style.name, "Test Style")

    def test_therapy_blank_image(self):
        self.assertEquals(self.therapy.image, None)

    def test_therapy_optional_empty(self):
        self.assertEqual(self.therapy.location, None)
        self.assertEqual(self.therapy.extra_requirements, None)

    # def test_therapy_image(self):
    #     image_path = '../staticfiles/images/'
    #     self.therapy.image = SimpleUploadedFile(name='noimage.png', content=open(image_path, 'rb').read(), content_type='image/png')
    #     self.assertEqual(self.therapy.location, None)

    def test_full_therapy_optional_fields(self):
        self.assertEqual(self.full_therapy.location, "My therapeutic offices")
        self.assertEqual(
            self.full_therapy.extra_requirements,
            "A list of extra requirements needed",
        )

    def test_full_therapy_style(self):
        self.assertEqual(self.full_therapy.style.__str__(), "Equipped Style")
        self.assertEqual(
            self.full_therapy.style.equipment,
            "List of any equipment required by this particular style",
        )

    def test_style_string(self):
        self.assertEqual(self.style.__str__(), "Test Style")

    def test_equipped_style_string(self):
        self.assertEqual(self.style_equipped.__str__(), "Equipped Style")

    def test_style_no_equipment(self):
        self.assertEqual(self.style.equipment, "")

    def test_style_equipment(self):
        self.assertEqual(
            self.style_equipped.equipment,
            "List of any equipment required by this particular style",
        )
