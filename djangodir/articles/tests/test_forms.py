from django.test import TestCase
from articles.forms import *
from articles.tests.helper import *

class FormsTest(TestCase):
    
    #以下SignupFormのテスト
    def test_signup_form(self):
        """有効なdataを渡されたSignupForm()がis_valid()を返すことを確認する"""
        username = 'form_test'
        password = 'signup_testing_password'
        signup_data = {
            'username': username,
            'password1': password,
            'password2': password
        }
        form = SignupForm(signup_data)

        self.assertTrue(form.is_valid())

    def test_signup_form_is_invalid_with_duplicate_data(self):
        """既に登録済みのusernameを引数として渡すと
        is_valid()==Falseとなることを確認する
        """
        user = get_test_user()
        duplicate_data = {
            'username': user.username,
            'password1': 'valid_test_password',
            'password2': 'valid_test_password'
        }
        form = SignupForm(duplicate_data)

        self.assertFalse(form.is_valid())

    def test_signup_form_is_invalid_with_invalid_data(self):
        """無効なdataを渡されたSignupForm()が
        is_valid() == False を返すことを確認する
        """
        valid_name = 'form_test'
        valid_password = 'valid_testing_password'
        #パスワードが短すぎるデータ
        short_password = 'test'
        short_pass_data = {
            'username': valid_name,
            'password1': short_password,
            'password2': short_password
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
        invalid_data_list = [short_pass_data, missing_username_data,
                             missing_password1_data, missing_password2_data]
        for invalid_data in invalid_data_list:
            with self.subTest(invalid_data=invalid_data):
                form = SignupForm(invalid_data)
                self.assertFalse(form.is_valid())
        
        #以下LoginFormのテスト
    def test_login_form_is_valid(self):
        """LoginForm()が有効なdataを引数として受け取って
        is_valid()==Trueとなることを確認する
        """
        username = 'form_test'
        password = 'signup_testing_password'
        signup_data = {
            'username': username,
            'password1': password,
            'password2': password
        }
        signup_form = SignupForm(data=signup_data)
        self.assertTrue(signup_form.is_valid())
        signup_form.save()
        login_data ={
            'username': username,
            'password': password
        }
        #テスト対象
        login_form = LoginForm(data=login_data)

        self.assertTrue(login_form.is_valid())

    def test_login_form_is_invalid_with_invalid_data(self):
        """LoginForm()が無効なdataを引数として受け取った場合
        is_valid()==Falseを返すことを確認する
        """
        #確認用のデータを登録する
        username = 'form_test'
        password = 'signup_testing_password'
        signup_data = {
            'username': username,
            'password1': password,
            'password2': password
        }
        signup_form = SignupForm(data=signup_data)
        self.assertTrue(signup_form.is_valid())
        signup_form.save()
        #無効なデータを用意
        #ユーザー名が未入力
        missing_username_data = {
            'password': password,
        }
        #passwordが未入力
        missing_password_data = {
            'username': username,
        }
        #パスワードが違っている
        wrong_password_data = {
            'username': username,
            'password': 'invalid_input',
        }
        invalid_data_list = [
            missing_username_data,
            missing_password_data,
            wrong_password_data
        ]
        for invalid_data in invalid_data_list:
            with self.subTest(invalid_data=invalid_data):
                form = LoginForm(data=invalid_data)
                self.assertFalse(form.is_valid())
