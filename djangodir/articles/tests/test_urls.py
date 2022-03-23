from django.test import TestCase
from django.urls import NoReverseMatch, resolve, exceptions
from articles.views import *

WRONG_URL_PATH = '/wrong_url_path/'

TEST_TITLE = '【TGC2022S/S】新庄剛志がサプライズ降臨「監督になって歩くのが一番鳥肌立つね！」ランウェイ中に“開幕投手”決断？（オリコン）'

class UrlsTest(TestCase):
    
    def test_resolve_article_response(self):
        '''pathからviews.article_responseが返されることを確認する'''
        view = resolve('/')
        self.assertEqual(view.func, article_response)

    def test_resolve_left_frame(self):
        '''pathからviews.left_frameが返されることを確認する'''
        view = resolve('/pages.html')
        self.assertEqual(view.func, left_frame)

    def test_resolve_init_frame(self):
        '''pathからviews.init_frameが返されることを確認する'''
        view = resolve('/src_link.html')
        self.assertEqual(view.func, init_link)

    def test_resolve_article_link(self):
        '''
        想定されるcategoryを含んだpath全てから
        views.article_linkが返されることを確認する
        '''
        for category in category_dict.keys():
            with self.subTest(category=category):
                view = resolve('/src_link?'+category)
                self.assertEqual(view.func, article_link)

    def test_resolve_loading(self):
        view = resolve('/loading')
        self.assertEqual(view.func, loading)
    
    def test_resolve_result(self):
        view = resolve('/result')
        self.assertEqual(view.func, result)

    def test_resolve_all_clear(self):
        '''
        想定されるcategoryを含んだpath全てから
        views.all_clearが返されることを確認する
        '''
        for category_jp in category_dict.values():
            with self.subTest(category=category_jp):
                view = resolve('/all_clear/?'+category_jp)
                self.assertEqual(view.func, all_clear)

    def test_resolve_eval_good(self):
        '''
        想定されるcategoryを含んだpath全てから
        views.eval_goodが返されることを確認する
        '''
        for category in category_dict.keys():
            with self.subTest(category=category):
                view = resolve('/eval_good/?'+category+'/?dummy_title')
                self.assertEqual(view.func, eval_good)

    def test_fail_eval_good(self):
        view = resolve('/eval_good/?'+'sports'+'/?'+TEST_TITLE)
        self.assertEqual(view.func, eval_good)

    def test_resolve_eval_uninterested(self):
        '''
        想定されるcategoryを含んだpath全てから
        views.eval_uninterestedが返されることを確認する
        '''
        for category in category_dict.keys():
            with self.subTest(category=category):
                view = resolve('/eval_uninterested/?'+category+'/?dummy_title')
                self.assertEqual(view.func, eval_uninterested)

    def test_wrong_url(self):
        '''誤ったpathから例外が送出されることを確認'''
        with self.assertRaises(exceptions.Resolver404):
            resolve(WRONG_URL_PATH)