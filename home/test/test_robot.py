from django.test import TestCase
from http import HTTPStatus

# Create your tests here.


class RobotsTest(TestCase):
    def test_get(self):
        # Check if the 'robots.txt' appears on a GET request
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Check to see if the context is plain text
        self.assertEqual(response["content-type"], "text/plain")
        lines = response.content.decode().splitlines()
        # Make sure the user agent is the first line of the file
        self.assertEqual(lines[0], "User-Agent: *")

    def test_post(self):
        #  Check if the request is a POST - the method is NOT allowed
        response = self.client.post("/robots.txt")

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)


class SitemapTest(TestCase):
    def test_get(self):
        # Check if the 'sitemap.xml' appears on a GET request
        response = self.client.get("/sitemap.xml")

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # Check to see if the context is xml
        self.assertEqual(response["content-type"], "text/xml")

    def test_post(self):
        #  Check if the request is a POST - the method is NOT allowed
        response = self.client.post("/sitemap.xml")

        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
