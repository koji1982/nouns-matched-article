from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from articles.views import *

REQUEST_OK = 200

class ViewsTest(TestCase):

    def test_response_article_response(self):
        request = HttpRequest()
        actual_response = article_response(request)
        actual_html = actual_response.content.decode('utf8')
        expected_template = render_to_string('app/frame.html')
        self.assertEqual(actual_response.status_code, REQUEST_OK)
        self.assertEqual(actual_html, expected_template)