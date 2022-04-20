import re
from urllib.parse import urlencode
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from articles.views import *
from articles.tests.helper import *

REQUEST_OK = 200
STATUS_REDIRECT = 302
SIGNUP_SUCCESS_REDIRECT = 302
SIGNUP_FAILER_RESPONSE = 200
LOGIN_SUCCESS_REDIRECT = 302
LOGIN_FAILER_RESPONSE = 200
WRONG_CATEGORY = 'wrong_category'
WRONG_TITLE = 'wrong_title'

class ViewsTest(TestCase):

    #ログイン関連のエラーを回避するために一部のテストでは
    #テスト対象の関数の代わりにclient.get()またはclient.post()
    #を使用している。

    fixtures = ["test_articles.json"]

    def setUp(self):
        #views.pyのテストはUser,Preferenceが作成済み、ログイン済みの状態から開始する
        prepare_user_pref(self)

    def tearDown(self):
        self.client.logout()

    def test_article_response(self):
        """article_response()が'app/frame.html'の正常なレスポンス
        を返すことを確認する
        """
        request = get_request('/')
        function_response = frame(request)
        actual_html = function_response.content.decode('utf8')

        expected_template = render_to_string('app/frame.html')

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_html, expected_template)

    def test_login_process_get_response(self):
        """login_process()がGETでのリクエスト時に
        'app/login.html'の正常なレスポンスを返すことを確認する
        """
        function_response = login_process(get_request('/login'))
        actual_html = function_response.content.decode('utf8')
        actual_without_csrf = remove_csrf(actual_html)

        expected_template = self.client.get('/login')
        expected_html = expected_template.content.decode('utf8')
        expected_without_csrf = remove_csrf(expected_html)

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_login_process_post_valid_input(self):
        """login_process()がPOSTメソッドで有効な入力でログインすることを確認する"""
        #ログアウト状態にする
        self.client.logout()
        #ログインのためにパスワード有りのUserを作成する
        create_user_with_password()
        data = {
            'username': 'password_user',
            'password': 'valid_test_password'
        }
        response = self.client.post('/login', data=data)

        self.assertEqual(response.status_code, LOGIN_SUCCESS_REDIRECT)
        self.assertRedirects(response, '/')
        self.assertEqual(response.wsgi_request.user.username, data['username'])

    def test_login_process_post_invalid_input_fail(self):
        """login_process()が無効な入力の時にログイン失敗することを確認する"""
        #ログアウトする
        self.client.logout()
        #ログインしないことを確認するため、パスワード有りのUserを作成する
        create_user_with_password()
        not_exist_user_data = {
            'username': 'not_exist_user',
            'password': 'not_exist_password'
        }
        missing_name_data = {
            'password': 'valid_test_password'
        }
        missing_password_data = {
            'username': 'password_user'
        }
        wrong_password_data = {
            'username': 'password_user',
            'password': 'invalid_test_password'
        }
        invalid_data_list = [
            not_exist_user_data,
            missing_name_data,
            missing_password_data,
            wrong_password_data
        ]
        for invalid_data in invalid_data_list:
            with self.subTest(invalid_data=invalid_data):
                response = self.client.post('/login', data=invalid_data)
                self.assertEqual(response.status_code, LOGIN_FAILER_RESPONSE)
                self.assertTrue(response.wsgi_request.user.is_anonymous)

    def test_login_guest_user_redirect(self):
        """login_guest_user()が呼ばれるとゲストユーザーが作成され
        path'/'へリダイレクトされることを確認する
        """
        self.assertFalse(User.objects.filter(username='ゲスト').exists())

        response = self.client.post('/guest')
        
        self.assertEqual(response.status_code, LOGIN_SUCCESS_REDIRECT)
        self.assertRedirects(response, '/')
        self.assertTrue(User.objects.filter(username='ゲスト').exists())

    def test_logout_reopen_redirect(self):
        """logout_reopen()が呼ばれるとUserがログアウトして
        リダイレクトすることを確認
        """
        response = self.client.post('/logout')
        
        self.assertEqual(response.status_code, STATUS_REDIRECT)
        #ログイン画面にリダイレクトされる
        self.assertRedirects(response, '/login',
                             status_code=STATUS_REDIRECT)
        self.assertTrue(response.wsgi_request.user.is_anonymous)

    def test_signup_get_response(self):
        """signup()がリクエスト(GET)で呼ばれると'app/signup.html'の
        正常なレスポンスを返すことを確認する
        """
        request = get_request('/singup')
        function_response = signup(request)
        actual_html = function_response.content.decode('utf8')
        actual_without_csrf = remove_csrf(actual_html)
        
        expected_template = self.client.get('/signup')
        expected_html = expected_template.content.decode('utf8')
        expected_without_csrf = remove_csrf(expected_html)

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_signup_input_post_make_login_succeed(self):
        """signup()が有効な入力データと共に呼ばれると
        Userが作成されログイン可能になることを確認する
        """
        username = 'post_test'
        password = 'signup_testing_password'
        signup_data = {
            'username': username,
            'password1': password,
            'password2': password
        }
        login_data = {
            'username': username,
            'password': password
        }
        #ログインをテストするためにログアウト
        self.client.logout()
        #Userが存在しないことを確認
        self.assertFalse(User.objects.filter(username=username).exists())
        #ログインが失敗することを確認
        before_login_response = self.client.post('/signup_completed', login_data)
        self.assertEqual(before_login_response.status_code, LOGIN_FAILER_RESPONSE)
        self.assertTrue(before_login_response.wsgi_request.user.is_anonymous)
        
        #テスト対象
        function_response = self.client.post('/signup', signup_data)

        #responseがサインアップ成功後のリダイレクトであることと、
        #Userが作成されていることを確認
        self.assertEqual(function_response.status_code, SIGNUP_SUCCESS_REDIRECT)
        self.assertTrue(User.objects.filter(username=username).exists())
        #ログイン成功することを確認
        after_login_response = self.client.post('/login', login_data)
        self.assertEqual(after_login_response.status_code, LOGIN_SUCCESS_REDIRECT)
        self.assertEqual(after_login_response.wsgi_request.user.username, username)

    def test_signup_fail_with_invalid_data(self):
        """signup()が無効な入力データと共に呼ばれると
        Userは作成されずログインもできないことを確認する
        """
        valid_name = 'post_test'
        valid_password = 'valid_testing_password'
        #パスワードが短すぎるデータ
        short_password = 'test'
        short_pass_data = {
            'username': valid_name,
            'password1': short_password,
            'password2': short_password
        }
        #既にあるユーザー名のデータ
        duplicate_name = 'test_user'
        duplicate_data = {
            'username': duplicate_name,
            'password1': valid_password,
            'password2': valid_password
        }
        #ユーザー名が'ゲスト'の場合
        guest_name_data = {
            'username': 'ゲスト',
            'password1': valid_password,
            'password2': valid_password
        }
        #ユーザー名が未記入
        missing_username_data = {
            'password1': valid_password,
            'password2': valid_password
        }
        #password1が未記入
        missing_password1_data = {
            'username': valid_name,
            'password2': valid_password
        }
        #password2が未記入
        missing_password2_data = {
            'username': valid_name,
            'password1': valid_password
        }
        #二つのパスワードが違っている
        different_password_data = {
            'username': valid_name,
            'password1': valid_password,
            'password2': 'different_password'
        }
        invalid_signup_data = [short_pass_data, duplicate_data, guest_name_data,
                               missing_username_data,missing_password1_data,
                               missing_password2_data, different_password_data]
        for input_data in invalid_signup_data:
            with self.subTest(input_data=input_data):
                #ログインをテストするためにログアウト
                self.client.logout()
        
                #テスト対象用のリクエスト
                request = post_request_with_anonymous('/signup', data=input_data)
                #テスト対象関数
                function_response = signup(request)

                #responseがサインアップ失敗のstatus(再読み込みの200)であることを確認
                self.assertEqual(function_response.status_code, SIGNUP_FAILER_RESPONSE)

    def test_signup_completed_response(self):
        """signup_completed()が'app/signup_completed.html'の
        正常なレスポンスを返すことを確認する
        """
        url = reverse('articles:signup_completed')
        param_dict = {
            'username': 'test_username', 
            'password': '*' * len('valid_test_password')
        }
        param_in_url = urlencode(param_dict)
        url_with_parameters = f'{url}?{param_in_url}'
        function_response = signup_completed(get_request(url_with_parameters))
        actual_html = function_response.content.decode('utf8')
        actual_without_csrf = remove_csrf(actual_html)

        expected_templete = self.client.get(url_with_parameters)
        expected_html = expected_templete.content.decode('utf8')
        expected_without_csrf = remove_csrf(expected_html)

        self.assertEqual(function_response.status_code, REQUEST_OK)
        # self.assertEqual(actual_html, expected_html)
        self.assertEqual(actual_without_csrf, expected_without_csrf)


    def test_left_frame(self):
        """left_frame()が'app/pages.html'の
        正常なレスポンスを返すことを確認する
        """
        request = get_request('/pages')
        function_response = left_frame(request)
        actual_html = function_response.content.decode('utf8')
        actual_without_csrf = remove_csrf(actual_html)

        expected_template = render_to_string('app/pages.html', request=request)
        expected_without_csrf = remove_csrf(expected_template)

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_article_link_without_arg(self):
        """article_link()がcategory引数なしで呼ばれたとき
        'app/src_link.html'の正常なレスポンスを返すことを確認する
        """
        request = get_request_with_pref('/src_link')
        self.client.force_login(request.user)
        function_response = article_link(request)
        actual_html = function_response.content.decode('utf8')
        actual_without_csrf = remove_csrf(actual_html)

        expected_template = self.client.get('/src_link')
        expected_html = expected_template.content.decode('utf8')
        expected_without_csrf = remove_csrf(expected_html)

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_article_link(self):
        """article_link()がcategory引数を渡されて呼ばれたとき
        各カテゴリーの'app/src_link.html'の正常なレスポンス
        を返すことを確認する
        """
        for category in CATEGORY_DICT.keys():
            with self.subTest(category=category):
                path = '/src_link/'+category
                request = get_request(path)
                function_response = article_link(request, category)
                actual_html = function_response.content.decode('utf8')
                actual_without_csrf = remove_csrf(actual_html)

                context = {'category': category}
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
            article_link(HttpRequest(), WRONG_CATEGORY)

    def test_all_clear(self):
        """all_clear()が呼ばれた時に評価が消去されて
        リダイレクトされることを確認する
        """
        preference = Preference.objects.get(user=get_test_user())
        preference.good_ids = '1,2,3,4,5'
        preference.uninterested_ids = '6,7,8,9,10'
        preference.save()

        function_response = self.client.post('/all_clear')

        preference_after = Preference.objects.get(user=get_test_user())
        self.assertEqual(function_response.status_code, STATUS_REDIRECT)
        self.assertRedirects(function_response, '/src_link')
        self.assertEqual(preference_after.good_ids, '')
        self.assertEqual(preference_after.uninterested_ids, '')

    def test_loading(self):
        """loading()が呼ばれると'app/loading.html'の
        正常なレスポンスを返すことを確認する
        """
        function_response = loading(HttpRequest())
        actual_html = function_response.content.decode('utf8')

        expected_template = self.client.get('/loading')
        expected_html = expected_template.content.decode('utf8')

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_html, expected_html)

    def test_call_apply_choices_redirect(self):
        """call_apply_choices()が呼ばれたとき'/result_positive'に
        リダイレクトされていることを確認する
        """
        function_response = self.client.post('/call_apply_choices')

        self.assertEqual(function_response.status_code, STATUS_REDIRECT)
        self.assertRedirects(function_response, '/result_positive')

    def test_call_apply_choices_calc_match_rate(self):
        """call_apply_choices()が呼ばれたとき、
        記事評価から一致率が計算されていることを確認する
        """
        preference = Preference.objects.get(user=get_test_user())
        preference.good_ids = '1,2,3,4,5'
        preference.uninterested_ids = '6,7,8,9,10'
        preference.save()
        self.assertEqual(preference.recommended_id_rate_pair, '')
        self.assertEqual(preference.rejected_id_rate_pair, '')
        response_positive = self.client.get('/result_positive')
        self.assertEqual(response_positive.context['recommendations'], [])
        response_negative = self.client.get('/result_negative')
        self.assertEqual(response_negative.context['recommendations'], [])

        self.client.post('/call_apply_choices')

        preference_after = Preference.objects.get(user=get_test_user())
        self.assertNotEqual(preference_after.recommended_id_rate_pair, '')
        self.assertNotEqual(preference_after.rejected_id_rate_pair, '')
        response_positive = self.client.get('/result_positive')
        self.assertNotEqual(response_positive.context['recommendations'], [])
        response_negative = self.client.get('/result_negative')
        self.assertNotEqual(response_negative.context['recommendations'], [])

    def test_result_positive(self):
        """result_positive()が正常なレスポンスを返すことを確認する"""
        function_response = result_positive(get_request_with_pref('/result_positive'))
        actual_html = function_response.content.decode('utf8')

        expected_template = self.client.get('/result_positive')
        expected_html = expected_template.content.decode('utf8')

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_html, expected_html)

    def test_result_negative(self):
        """result_negative()が正常なレスポンスを返すことを確認する"""
        function_response = result_negative(get_request_with_pref('/result_negative'))
        actual_html = function_response.content.decode('utf8')

        expected_template = self.client.get('/result_negative')
        expected_html = expected_template.content.decode('utf8')
        
        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_html, expected_html)

    def test_category_clear(self):
        """category_clear()が呼ばれると
        同じカテゴリーの同じページを開くことを確認する
        """
        for category_jp in CATEGORY_DICT.values():
            with self.subTest(category=category_jp):
                path = '/category_clear/'+category_jp
                request = get_request(path)
                function_response = category_clear(request, category_jp)
                actual_html = function_response.content.decode('utf8')
                actual_without_csrf = remove_csrf(actual_html)

                context = {'category': category_jp}
                expected_template = self.client.post(path, context)
                expected_html = expected_template.content.decode('utf8')
                expected_without_csrf = remove_csrf(expected_html)

                self.assertEqual(function_response.status_code, REQUEST_OK)
                self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_category_clear_with_wrong_category(self):
        """category_clear()が間違ったカテゴリー名を引数として
        渡されて呼ばれたときエラーを送出することを確認する
        """
        with self.assertRaises(KeyError):
            category_clear(HttpRequest(), WRONG_CATEGORY)

    def test_eval_good(self):
        """eval_good()が呼ばれたとき
        同じカテゴリーの同じページを開く（更新する）ことを確認する
        """
        for category in CATEGORY_DICT.keys():
            with self.subTest(category=category):
                #各カテゴリーの先頭のデータを取り出してテストデータとする
                test_article = Article.objects.filter(category=category)[0]
                #テスト対象関数のurlパス
                path = '/eval_good/'+category+'/'+test_article.title
                #テストに必要なrequest,userを用意するヘルパー関数
                request = get_request(path)
                #テスト対象の関数呼び出しとその結果のhtml取り出し
                function_response = eval_good(request, category, test_article.title)
                actual_html = function_response.content.decode('utf8')
                actual_without_csrf = remove_csrf(actual_html)
                #テスト対象の関数が呼ばれるとtest_articleのeval_goodフィールドが
                #Trueになるため、モデルにアクセスして状態を戻す
                Preference.objects.get(user=request.user).all_clear()
                #比較用のhtml取り出し
                context = {'category': category}
                expected_template = self.client.post(path, context)
                expected_html = expected_template.content.decode('utf8')
                expected_without_csrf = remove_csrf(expected_html)

                self.assertEqual(function_response.status_code, REQUEST_OK)
                self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_eval_good_with_wrong_args(self):
        """eval_good()に誤った引数を渡すとエラーを送出することを確認する"""
        test_article = Article.objects.filter(category='domestic')[0]
        correct_title = test_article.title
        path = '/eval_good/'+test_article.category+'/'+test_article.title
        request = get_request(path)

        #誤ったcategoryを渡すとKeyErrorをraiseする
        with self.assertRaises(KeyError):
            eval_good(request, WRONG_CATEGORY, correct_title)
        #誤ったArticle.titleを渡すとDoesNotExistをraiseする
        self.assertNotEqual(correct_title, WRONG_TITLE)
        with self.assertRaises(Article.DoesNotExist):
            eval_good(request, 'domestic', WRONG_TITLE)
        #誤ったcategoryと誤ったArticle.titleを渡した時にDoesNotExistをraiseする
        with self.assertRaises(Article.DoesNotExist):
            eval_good(HttpRequest, WRONG_CATEGORY, WRONG_TITLE)

    def test_eval_uninterested(self):
        """eval_uninterested()が呼ばれたとき
        同じカテゴリーの同じページを開く（更新する）ことを確認する"""
        for category in CATEGORY_DICT.keys():
            with self.subTest(category=category):
                #各カテゴリーの先頭のデータを取り出してテストデータとする
                test_article = Article.objects.filter(category=category)[0]
                #テスト対象のurlパス
                path = '/eval_uninterested/'+category+'/'+test_article.title
                #テストに必要なrequest,userを用意するヘルパー関数
                request = get_request(path)
                #テスト対象の関数呼び出しとその結果のhtml取り出し
                function_response = eval_uninterested(request, category, test_article.title)
                actual_html = function_response.content.decode('utf8')
                actual_without_csrf = remove_csrf(actual_html)
                #テスト対象の関数が呼ばれるとtest_articleのeval_uninterestedフィールドが
                #Trueになるため、モデルにアクセスして状態を戻す
                Preference.objects.get(user=request.user).all_clear()
                #比較用のhtml取り出し
                context = {'category': category}
                expected_template = self.client.post(path, context)
                expected_html = expected_template.content.decode('utf8')
                expected_without_csrf = remove_csrf(expected_html)

                self.assertEqual(function_response.status_code, REQUEST_OK)
                self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_eval_uninterested_with_wrong_category_correct_title(self):
        """eval_uninterested()に誤った引数を渡すとエラーを送出することを確認する"""
        test_article = Article.objects.filter(category='domestic')[0]
        correct_title = test_article.title
        path = '/eval_good/'+test_article.category+'/'+test_article.title
        request = get_request(path)
        #誤ったcategoryを渡すとKeyErrorをraiseすることを確認する
        with self.assertRaises(KeyError):
            eval_uninterested(request, WRONG_CATEGORY, correct_title)
        #誤ったArticle.titleを渡すとDoesNotExistをraiseすることを確認する
        with self.assertRaises(Article.DoesNotExist):
            eval_uninterested(request, 'domestic', WRONG_TITLE)
        #誤ったcategoryと誤ったArticle.titleを渡した時にDoesNotExistをraiseすることを確認する
        with self.assertRaises(Article.DoesNotExist):
            eval_uninterested(request, WRONG_CATEGORY, WRONG_TITLE)
