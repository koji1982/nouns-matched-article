import re
from django.test import TestCase
from django.http import HttpRequest
from django.template import Context, Template
from django.template.loader import render_to_string
from articles.views import *
from articles.tests.helper import remove_csrf

REQUEST_OK = 200
WRONG_CATEGORY = 'wrong_category'
WRONG_TITLE = 'wrong_title'

class ViewsTest(TestCase):

    fixtures = ["test_articles.json"]

    def test_article_response(self):
        request = HttpRequest()
        function_response = article_response(request)
        actual_html = function_response.content.decode('utf8')

        expected_template = render_to_string('app/frame.html')

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_html, expected_template)

    def test_left_frame(self):
        request = HttpRequest()
        function_response = left_frame(request)
        actual_html = function_response.content.decode('utf8')
        actual_without_csrf = remove_csrf(actual_html)

        expected_template = render_to_string('app/pages.html', request=request)
        expected_without_csrf = remove_csrf(expected_template)

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_init_link(self):
        request = HttpRequest()
        function_response = init_link(request)
        actual_html = function_response.content.decode('utf8')
        actual_without_csrf = remove_csrf(actual_html)

        context = {'category': 'domestic'}
        expected_template = self.client.get('/src_link.html', context)
        expected_html = expected_template.content.decode('utf8')
        expected_without_csrf = remove_csrf(expected_html)

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_article_link(self):
        for category in category_dict.keys():
            with self.subTest(category=category):
                request = HttpRequest()
                function_response = article_link(request, category)
                actual_html = function_response.content.decode('utf8')
                actual_without_csrf = remove_csrf(actual_html)

                context = {'category': category}
                path = '/'+category
                expected_template = self.client.get(path, context)
                expected_html = expected_template.content.decode('utf8')
                expected_without_csrf = remove_csrf(expected_html)

                self.assertEqual(function_response.status_code, REQUEST_OK)
                self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_article_link_with_wrong_category(self):
        """article_link()に誤った引数(category)が渡された場合に
        例外が出されることを確認する
        """
        with self.assertRaises(KeyError):
            article_link(HttpRequest, WRONG_CATEGORY)

    def test_all_clear(self):
        for category_jp in category_dict.values():
            with self.subTest(category=category_jp):
                request = HttpRequest()
                function_response = all_clear(request, category_jp)
                actual_html = function_response.content.decode('utf8')
                actual_without_csrf = remove_csrf(actual_html)

                context = {'category': category_jp}
                path = '/all_clear/'+category_jp
                expected_template = self.client.post(path, context)
                expected_html = expected_template.content.decode('utf8')
                expected_without_csrf = remove_csrf(expected_html)

                self.assertEqual(function_response.status_code, REQUEST_OK)
                self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_all_clear_with_wrong_category(self):
        with self.assertRaises(KeyError):
            all_clear(HttpRequest, WRONG_CATEGORY)

    def test_eval_good(self):
        for category in category_dict.keys():
            with self.subTest(category=category):
                #各カテゴリーの先頭のデータを取り出してテストデータとする
                test_article = Article.objects.filter(category=category)[0]
                #テスト対象の関数呼び出しとその結果のhtml取り出し
                function_response = eval_good(HttpRequest(), category, test_article.title)
                actual_html = function_response.content.decode('utf8')
                actual_without_csrf = remove_csrf(actual_html)
                #テスト対象の関数が呼ばれるとtest_articleのeval_goodフィールドが
                #Trueになるため、モデルにアクセスして状態を戻す
                test_article.clear_evaluation()
                #比較用のhtml取り出し
                context = {'category': category}
                path = '/eval_good/'+category+'/'+test_article.title
                expected_template = self.client.post(path, context)
                expected_html = expected_template.content.decode('utf8')
                expected_without_csrf = remove_csrf(expected_html)

                self.assertEqual(function_response.status_code, REQUEST_OK)
                self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_eval_good_with_wrong_category_correct_title(self):
        """eval_good()に誤ったcategoryを渡すとKeyErrorをraiseすることを確認する"""
        test_article = Article.objects.filter(category='domestic')[0]
        correct_title = test_article.title
        with self.assertRaises(KeyError):
            eval_good(HttpRequest, WRONG_CATEGORY, correct_title)

    def test_eval_good_with_correct_category_wrong_title(self):
        """eval_good()に誤ったArticle.titleを渡すとDoesNotExistをraiseすることを確認する"""
        with self.assertRaises(Article.DoesNotExist):
            eval_good(HttpRequest, 'domestic', WRONG_TITLE)

    def test_eval_good_with_wrong_category_wrong_title(self):
        """eval_good()に誤ったcategoryと誤ったArticle.titleを渡した時に
        DoesNotExistをraiseすることを確認する
        """
        with self.assertRaises(Article.DoesNotExist):
            eval_good(HttpRequest, WRONG_CATEGORY, WRONG_TITLE)

    def test_eval_uninterested(self):
        for category in category_dict.keys():
            with self.subTest(category=category):
                #各カテゴリーの先頭のデータを取り出してテストデータとする
                test_article = Article.objects.filter(category=category)[0]
                #テスト対象の関数呼び出しとその結果のhtml取り出し
                function_response = eval_uninterested(HttpRequest(), category, test_article.title)
                actual_html = function_response.content.decode('utf8')
                actual_without_csrf = remove_csrf(actual_html)
                #テスト対象の関数が呼ばれるとtest_articleのeval_uninterestedフィールドが
                #Trueになるため、モデルにアクセスして状態を戻す
                test_article.clear_evaluation()
                #比較用のhtml取り出し
                context = {'category': category}
                path = '/eval_uninterested/'+category+'/'+test_article.title
                expected_template = self.client.post(path, context)
                expected_html = expected_template.content.decode('utf8')
                expected_without_csrf = remove_csrf(expected_html)

                self.assertEqual(function_response.status_code, REQUEST_OK)
                self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_eval_uninterested_with_wrong_category_correct_title(self):
        """eval_uninterested()に誤ったcategoryを渡すとKeyErrorをraiseすることを確認する"""
        test_article = Article.objects.filter(category='domestic')[0]
        correct_title = test_article.title
        with self.assertRaises(KeyError):
            eval_uninterested(HttpRequest, WRONG_CATEGORY, correct_title)

    def test_eval_uninterested_with_correct_category_wrong_title(self):
        """eval_uninterested()に誤ったArticle.titleを渡すとDoesNotExistをraiseすることを確認する"""
        with self.assertRaises(Article.DoesNotExist):
            eval_uninterested(HttpRequest, 'domestic', WRONG_TITLE)

    def test_eval_uninterested_with_wrong_category_wrong_title(self):
        """
        eval_uninterested()に誤ったcategoryと誤ったArticle.titleを渡した時に
        DoesNotExistをraiseすることを確認する
        """
        with self.assertRaises(Article.DoesNotExist):
            eval_uninterested(HttpRequest, WRONG_CATEGORY, WRONG_TITLE)
