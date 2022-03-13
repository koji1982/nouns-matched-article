from django.test import TestCase
from django.http import HttpRequest
from articles.templatetags.external_functions import apply_choices
from articles.models import Article

class ExternalFunctionsTest(TestCase):

    fixtures = ['test_articles.json']

    def test_apply_choices(self):
        test_article = Article.objects.filter(category='domestic')[0]
        test_article.evaluate(Article.EVAL_GOOD)

        apply_choices(HttpRequest())

        results = Article.objects.filter(rate__gt=0.0)
        self.assertTrue(0<results.count())
