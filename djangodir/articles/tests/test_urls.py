from django.test import TestCase
from django.urls import NoReverseMatch, resolve, exceptions
from articles.views import *

WRONG_URL_PATH = '/wrong_url_path/'

class UrlsTest(TestCase):
    
    def test_resolve_article_response(self):
        '''path'/'からviews.article_responseが返されることを確認する'''
        view = resolve('/')
        self.assertEqual(view.func, frame)

    def test_resolve_login(self):
        '''path'/login'からview.loginが返されることを確認する'''
        view = resolve('/login')
        self.assertEqual(view.func, login_process)

    def test_resolve_login_guest_user(self):
        '''path'/guest'からview.guest_loginが返されることを確認する'''
        view = resolve('/guest')
        self.assertEqual(view.func, login_guest_user)

    def test_resolve_signup(self):
        '''path'/signup'からview.signupが返されることを確認する'''
        view = resolve('/signup')
        self.assertEqual(view.func, signup)

    def test_resolve_signup_completed(self):
        '''path'signup_completed'からview.signup_completedが返されることを確認する'''
        view = resolve('/signup_completed')
        self.assertEqual(view.func, signup_completed)

    def test_resolve_logout_reopen(self):
        '''path'/logout'からviews.logout_reopenが返されることを確認する'''
        view = resolve('/logout')
        self.assertEqual(view.func, logout_reopen)

    def test_resolve_left_frame(self):
        '''path'/pages'からviews.left_frameが返されることを確認する'''
        view = resolve('/pages')
        self.assertEqual(view.func, left_frame)

    def test_resolve_article_link_without_arg(self):
        """引数無しのpath'/src_link'からviews.article_linkが返されることを確認する"""
        view = resolve('/src_link')
        self.assertEqual(view.func, article_link)

    def test_resolve_article_link(self):
        '''categoryを含んだpath'/src_link/'全てから
        views.article_linkが返されることを確認する
        '''
        for category in CATEGORY_DICT.keys():
            with self.subTest(category=category):
                view = resolve('/src_link/?'+category)
                self.assertEqual(view.func, article_link)

    def test_resolve_all_clear(self):
        """path'/all_clear'からviews.all_clearが返されることを確認する"""
        view = resolve('/all_clear')
        self.assertEqual(view.func, all_clear)
        
    def test_resolve_loading(self):
        """path'/loading'からviews.loadingが返されることを確認する"""
        view = resolve('/loading')
        self.assertEqual(view.func, loading)
    
    def test_resolve_result_positive(self):
        """path'/result_positive'からviews.result_positiveが返されることを確認する"""
        view = resolve('/result_positive')
        self.assertEqual(view.func, result_positive)

    def test_resolve_result_negative(self):
        """path'/result_negative'からviews.result_negativeが
        返されることを確認する
        """
        view = resolve('/result_negative')
        self.assertEqual(view.func, result_negative)

    def test_resolve_graph(self):
        """path'/graph'からviews.graphが
        返されることを確認する
        """
        view = resolve('/graph')
        self.assertEqual(view.func, result_graph)

    def test_resolve_category_clear(self):
        '''想定されるcategoryを含んだpath'/category_clear'全てから
        views.category_clearが返されることを確認する
        '''
        for category_jp in CATEGORY_DICT.values():
            with self.subTest(category=category_jp):
                view = resolve('/category_clear/?'+category_jp)
                self.assertEqual(view.func, category_clear)

    def test_resolve_eval_good(self):
        '''想定されるcategoryを含んだpath'/eval_good/'全てから
        views.eval_goodが返されることを確認する
        '''
        for category in CATEGORY_DICT.keys():
            with self.subTest(category=category):
                view = resolve('/eval_good/?'+category+'/?dummy_title')
                self.assertEqual(view.func, eval_good)

    def test_resolve_eval_uninterested(self):
        '''想定されるcategoryを含んだpath'/eval_uninterested/'全てから
        views.eval_uninterestedが返されることを確認する
        '''
        for category in CATEGORY_DICT.keys():
            with self.subTest(category=category):
                view = resolve('/eval_uninterested/?'+category+'/?dummy_title')
                self.assertEqual(view.func, eval_uninterested)

    def test_wrong_url(self):
        '''誤ったpathから例外が送出されることを確認'''
        with self.assertRaises(exceptions.Resolver404):
            resolve(WRONG_URL_PATH)