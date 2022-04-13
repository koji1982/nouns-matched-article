from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from articles.tests.test_views import *
from articles.tests.helper import *


class ScenarioTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument('-headless')
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_user_open_eval_apply_result(self):
        # options = Options()
        # options.add_argument('-headless')
        # driver = webdriver.Firefox(options=options)

        # driver.get(self.live_server_url)
        # print(self.live_server_url)
        # print(self.selenium.page_source)
        # driver.quit()

        self.selenium.get(self.live_server_url + '/')
        print(self.selenium.page_source)

        register_link = self.selenium.find_element_by_link_text('新規登録')
        register_link.click()
        print(self.selenium.page_source)

        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('browser_test_user')
        password1_input = self.selenium.find_element_by_name('password1')
        password1_input.send_keys('valid_browser_test_password')
        password2_input = self.selenium.find_element_by_name('password2')
        password2_input.send_keys('valid_browser_test_password')
        register_button = self.selenium.find_element_by_name('register_button')
        register_button.submit()
        self.selenium.implicitly_wait(10)
        print(self.live_server_url)


        #ログイン画面からゲストとしてログインする
        login_view = resolve('/login')
        login_view_response = login_view.func(get_request('/login'))
        

        #urlを指定してページを開く
        view = resolve('/')
        function_response = view.func(get_request('/'))
        actual_html = function_response.content.decode('utf8')

        expected_template = render_to_string('app/frame.html')

        self.assertEqual(function_response.status_code, REQUEST_OK)
        self.assertEqual(actual_html, expected_template)
        #選択ページ(国内)で上から1番目と3番目の記事にgoodの評価をする
        
        #カテゴリーを国際に切り替える

        #2番目と3番目の記事にuninterestedの評価をする

        #反映ボタンを押す

        #結果のページを開く
