from django.test import TestCase
from articles.models import Article

class ModelsTest(TestCase):

    fixtures = ["test_articles.json"]

    def test_evalulate_good(self):
        """evaluate()"""
        test_article = Article.objects.filter(category='domestic')[0]
        self.assertEqual(test_article.evaluation, Article.NOT_EVALUATED)
        test_article.evaluate(Article.EVAL_GOOD)
        self.assertEquals(test_article.evaluation, Article.EVAL_GOOD)

    def test_evaluate_good_clears_value_with_even_call(self):
        test_article = Article.objects.filter(category='domestic')[0]
        self.assertEqual(test_article.evaluation, Article.NOT_EVALUATED)
        test_article.evaluate(Article.EVAL_GOOD)
        test_article.evaluate(Article.EVAL_GOOD)
        self.assertEquals(test_article.evaluation, Article.NOT_EVALUATED)

    def test_evaluate_good_turns_eval_uninterested_to_eval_good(self):
        test_article = Article.objects.filter(category='domestic')[0]
        test_article.evaluate(Article.EVAL_UNINTERESTED)
        self.assertEqual(test_article.evaluation, Article.EVAL_UNINTERESTED)
        test_article.evaluate(Article.EVAL_GOOD)
        self.assertEqual(test_article.evaluation, Article.EVAL_GOOD)
        
    def test_evaluate_uninterested(self):
        test_article = Article.objects.filter(category='domestic')[0]
        self.assertEqual(test_article.evaluation, Article.NOT_EVALUATED)
        test_article.evaluate(Article.EVAL_UNINTERESTED)
        self.assertEqual(test_article.evaluation, Article.EVAL_UNINTERESTED)

    def test_evaluate_uninterested_clears_value_even_call(self):
        test_article = Article.objects.filter(category='domestic')[0]
        test_article.evaluate(Article.EVAL_UNINTERESTED)
        self.assertEqual(test_article.evaluation, Article.EVAL_UNINTERESTED)
        test_article.evaluate(Article.EVAL_UNINTERESTED)
        self.assertEqual(test_article.evaluation, Article.NOT_EVALUATED)

    def test_evaluate_uninterested_turns_eval_good_to_eval_uninterested(self):
        test_article = Article.objects.filter(category='domestic')[0]
        test_article.evaluate(Article.EVAL_GOOD)
        self.assertEqual(test_article.evaluation, Article.EVAL_GOOD)
        test_article.evaluate(Article.EVAL_UNINTERESTED)
        self.assertEqual(test_article.evaluation, Article.EVAL_UNINTERESTED)

    def test_evaluate_raises_error_with_wrong_args(self):
        """evaluate()はEVAL_GOOD=1,EVAL_UNINTERESTED=2,以外の引数を
        受け取らないことを確認する
        """
        test_article = Article.objects.filter(category='domestic')[0]
        with self.assertRaises(ValueError):
            test_article.evaluate(-5000)
        with self.assertRaises(ValueError):
            test_article.evaluate(-1)
        with self.assertRaises(ValueError):
            test_article.evaluate(0)
        with self.assertRaises(ValueError):
            test_article.evaluate(3)
        with self.assertRaises(ValueError):
            test_article.evaluate(10000)
