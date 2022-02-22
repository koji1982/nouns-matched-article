from django.test import TestCase
from django.urls import resolve
from articles.views import *

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
            view = resolve('/src_link?'+category)
            self.assertEqual(view.func, article_link)
    
    def test_resolve_all_clear(self):
        '''
        想定されるcategoryを含んだpath全てから
        views.all_clearが返されることを確認する
        '''
        for category_jp in category_dict.values():
            view = resolve('/all_clear/?'+category_jp)
            self.assertEqual(view.func, all_clear)

    def test_resolve_eval_good(self):
        '''
        想定されるcategoryを含んだpath全てから
        views.eval_goodが返されることを確認する
        '''
        for category in category_dict.keys():
            view = resolve('/eval_good/?'+category+'/?dummy_title')
            self.assertEqual(view.func, eval_good)

    def test_resolve_eval_uninterested(self):
        '''
        想定されるcategoryを含んだpath全てから
        views.eval_uninterestedが返されることを確認する
        '''
        for category in category_dict.keys():
            view = resolve('/eval_uninterested/_'+category+'/?dummy_title')
            self.assertEqual(view.func, eval_uninterested)