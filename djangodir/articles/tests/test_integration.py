from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from django.template.loader import render_to_string
from articles.tests.helper import remove_csrf, get_request
from articles.views import *


class IntegrationTest(TestCase):

    fixtures = ["test_articles.json"]

    def test_routing_response_from_slash(self):
        """urlパス'/'から返されるview関数にリクエストを送り
        app/frame.htmlを取得する
        """
        view = resolve('/')
        response = view.func(get_request('/'))
        actual_html = response.content.decode('utf8')

        expected_html = render_to_string('app/frame.html')

        self.assertEqual(actual_html, expected_html)

    def test_routing_response_from_pages(self):
        """"""
        path = '/pages'
        actual_without_csrf = self.get_actual_html_with_user(path)

        expected_html = render_to_string('app/pages.html', request=get_request(path))
        expected_template = self.client.get(path)
        # expected_html = expected_template.content.decode('utf8')
        expected_without_csrf = remove_csrf(expected_html)

        self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_routing_response_from_src_link(self):
        """
        """
        path = '/src_link'
        actual_without_csrf = self.get_actual_html_with_user(path)

        expected_without_csrf = self.get_expected_html(path)

        self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_routing_response_from_src_link_with_category(self):
        for category in CATEGORY_DICT.keys():
            with self.subTest(category=category):
                path = '/src_link?'+category
                actual_without_csrf = self.get_actual_html(path, category)

                expected_without_csrf = self.get_expected_html('/'+category, category)

                self.assertEqual(actual_without_csrf, expected_without_csrf)

    # def test_routing_response_from_all_clear(self):
    #     for category in CATEGORY_DICT.keys():
    #         with self.subTest(category=category):
    #             category_jp = get_category_jp(category)
    #             path = '/all_clear/?'+category_jp
    #             actual_without_csrf = self.get_actual_html(path, category_jp)

    #             path_for_expected = '/all_clear/'+category_jp
    #             expected_without_csrf = self.get_expected_html(path_for_expected, category_jp)

    #             self.assertEqual(actual_without_csrf, expected_without_csrf)

    # def test_routing_response_from_eval_good(self):
    #     for category in CATEGORY_DICT.keys():
    #         with self.subTest(category=category):
    #             test_article = Article.objects.filter(category=category)[0]
    #             path = '/eval_good/?'+category+'/?'+test_article.title
    #             actual_without_csrf = self.get_actual_html(path, category, test_article)
    #             #テスト対象の関数が呼ばれるとtest_articleのeval_goodフィールドが
    #             #Trueになるため、モデルにアクセスして状態を戻す
    #             test_article.clear_evaluation()

    #             path_for_expected = '/eval_good/'+category+'/'+test_article.title
    #             expected_without_csrf = self.get_expected_html(path_for_expected, category)

    #             self.assertEqual(actual_without_csrf, expected_without_csrf)

    # def test_routing_response_from_eval_uninterested(self):
    #     for category in CATEGORY_DICT.keys():
    #         with self.subTest(category=category):
    #             test_article = Article.objects.filter(category=category)[0]
    #             path = '/eval_uninterested/?'+category+'/?'+test_article.title
    #             actual_without_csrf = self.get_actual_html(path, category, test_article)
    #             #テスト対象の関数が呼ばれるとtest_articleのeval_uninterestedフィールドが
    #             #Trueになるため、モデルにアクセスして状態を戻す
    #             test_article.clear_evaluation()

    #             path_for_expected = '/eval_uninterested/'+category+'/'+test_article.title
    #             expected_without_csrf = self.get_expected_html(path_for_expected, category)

    #             self.assertEqual(actual_without_csrf, expected_without_csrf)

    # def test_process_item_to_extract_nouns
    
    def get_actual_html_with_user(self, path):
        view = resolve(path)
        request = get_request(path)
        response = view.func(request)
        actual_html = response.content.decode('utf8')
        return remove_csrf(actual_html)
    
    def get_actual_html(self, path, category=None, test_article=None):
        view = resolve(path)
        response = None
        if category is None:
            response = view.func(HttpRequest())
        elif test_article is None:
            response = view.func(HttpRequest(), category)
        # else:
        #     response = view.func(HttpRequest(), category, test_article.title)
        actual_html = response.content.decode('utf8')
        return remove_csrf(actual_html)

    def get_expected_html(self, path, category='domestic'):
        context={'category':category}
        expected_template = self.client.post(path, context)
        expected_html = expected_template.content.decode('utf8')
        return remove_csrf(expected_html)
