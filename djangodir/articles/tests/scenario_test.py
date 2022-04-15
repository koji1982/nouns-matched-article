from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from articles.tests.test_views import *
from articles.tests.helper import *


class ScenarioTest(StaticLiveServerTestCase):

    fixtures = ["test_articles.json"]

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
        """ユーザー視点で、最初のページから、ユーザー登録、ログイン、記事を評価、
        評価を元に記事内の名詞の一致率を算出、算出された率を確認、ログアウト、
        という流れをテストする
        """
        #最初のページ(非ログイン状態だとログインページ)を開く
        self.selenium.get(self.live_server_url + '/')
        #ユーザー新規登録画面に移動する
        register_link = self.selenium.find_element_by_link_text('新規登録')
        register_link.click()
        #ユーザー名とパスワードを登録する
        test_username = 'browser_test_user'
        test_password = 'valid_browser_test_password'
        username_signup_form = self.selenium.find_element_by_name('username')
        username_signup_form.send_keys(test_username)
        password1_signup_form = self.selenium.find_element_by_name('password1')
        password1_signup_form.send_keys(test_password)
        password2_signup_form = self.selenium.find_element_by_name('password2')
        password2_signup_form.send_keys(test_password)
        register_button = self.selenium.find_element_by_name('register_button')
        register_button.click()
        self.selenium.implicitly_wait(10)
        #登録完了でログイン画面へ戻る
        signup_ok_button = self.selenium.find_element_by_name('signup_ok')
        signup_ok_button.click()

        #ユーザーが作成されているかを確認
        self.assertTrue(User.objects.filter(username=test_username).exists())

        #ログイン画面からログインする
        username_login_form = self.selenium.find_element_by_name('username')
        username_login_form.send_keys(test_username)
        password_login_form = self.selenium.find_element_by_name('password')
        password_login_form.send_keys(test_password)
        login_button = self.selenium.find_element_by_name('login_button')
        login_button.click()
        self.selenium.implicitly_wait(10)
        
        #Preferenceが作成されているか確認
        user = User.objects.get(username=test_username)
        self.assertTrue(Preference.objects.filter(username=user).exists())

        #右側のフレームを選択する
        right_frame = self.selenium.find_element_by_id('right_frame')
        self.selenium.switch_to.frame(right_frame)
        #選択ページ(国内)で上から1番目と3番目の記事にgoodの評価をする
        domestic_1_good = self.selenium.find_element_by_id('1_good')
        self.assertFalse(domestic_1_good.is_selected())
        domestic_1_good.click()
        domestic_3_good = self.selenium.find_element_by_id('3_good')
        domestic_3_good.click()

        #記事がクリックされていることを確認
        domestic_1_good_clicked = self.selenium.find_element_by_id('1_good')
        self.assertTrue(domestic_1_good_clicked.is_selected())
        domestic_3_good_clicked = self.selenium.find_element_by_id('3_good')
        self.assertTrue(domestic_3_good_clicked.is_selected())

        #カテゴリーを国際に切り替える
        world_link = self.selenium.find_element_by_link_text('国際')
        world_link.click()

        #2番目と3番目の記事にuninterestedの評価をする
        world_2_uninterested = self.selenium.find_element_by_id('2_uninterested')
        world_2_uninterested.click()
        world_3_uninterested = self.selenium.find_element_by_id('3_uninterested')
        world_3_uninterested.click()

        #記事がクリックされていることを確認
        world_2_uninterested_clicked = self.selenium.find_element_by_id('2_uninterested')
        self.assertTrue(world_2_uninterested_clicked.is_selected())
        world_3_uninterested_clicked = self.selenium.find_element_by_id('3_uninterested')
        self.assertTrue(world_3_uninterested_clicked.is_selected())
        
        #左側のフレームを選択する
        self.selenium.switch_to.parent_frame()
        left_frame = self.selenium.find_element_by_id('left_frame')
        self.selenium.switch_to.frame(left_frame)
        #反映ボタンをクリックする。
        apply_button = self.selenium.find_element_by_id('apply')
        apply_button.click()

        #右側のフレームへ移動して結果のページを確認する
        self.selenium.switch_to.parent_frame()
        right_frame = self.selenium.find_element_by_id('right_frame')
        self.selenium.switch_to.frame(right_frame)

        #反映ボタンクリック時の処理が終わるまで明示的待機
        WebDriverWait(self.selenium, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "result_rate"))
        )
        #推奨候補ページの一致率が計算されて降順に並んでいることを確認する
        result_rate_list = self.selenium.find_elements_by_class_name('result_rate')
        previous_value = result_rate_list.pop(0)
        for result_rate in result_rate_list:
            with self.subTest(result_rate=result_rate):
                self.assertGreaterEqual(float(previous_value.text.strip()),
                                        float(result_rate.text.strip()))
                previous_value = result_rate

        #左側のフレームへ移動して'除外候補'リンクをクリックする
        self.selenium.switch_to.parent_frame()
        left_frame = self.selenium.find_element_by_id('left_frame')
        self.selenium.switch_to.frame(left_frame)
        recommend_link = self.selenium.find_element_by_link_text('除外候補')
        recommend_link.click()

        #右側の画面に戻る
        self.selenium.switch_to.parent_frame()
        right_frame = self.selenium.find_element_by_id('right_frame')
        self.selenium.switch_to.frame(right_frame)

        #除外候補の側も一致率が計算されて降順に並んでいることを確認する
        result_rate_list = self.selenium.find_elements_by_class_name('result_rate')
        previous_value = result_rate_list.pop(0)
        for result_rate in result_rate_list:
            with self.subTest(result_rate=result_rate):
                self.assertGreaterEqual(float(previous_value.text.strip()),
                                        float(result_rate.text.strip()))
                previous_value = result_rate

        #ログアウトでログイン画面に戻って終了
        self.selenium.switch_to.parent_frame()
        left_frame = self.selenium.find_element_by_id('left_frame')
        self.selenium.switch_to.frame(left_frame)

        logout_button = self.selenium.find_element_by_id('logout_button')
        logout_button.click()
        self.selenium.switch_to.parent_frame()
        #ログイン画面が表示されていることを確認
        self.selenium.implicitly_wait(10)
        title = self.selenium.find_element_by_tag_name("title")
        self.assertEqual(title.get_attribute('textContent'), 'ログイン画面')

