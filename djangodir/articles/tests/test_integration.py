from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from django.template.loader import render_to_string
from articles.tests.helper import *
from articles.views import *
from articles.tests.test_views import *


class IntegrationTest(TestCase):

    fixtures = ["test_articles.json"]

    def setUp(self):
        prepare_user_pref(self)

    def tearDown(self):
        self.client.logout()

    def test_routing_response_from_frame(self):
        """urlパス'/'から返されるview関数にリクエストを送り
        app/frame.htmlを取得することを確認する
        """
        view = resolve('/frame')
        response = view.func(get_request('/frame'))
        actual_html = response.content.decode('utf8')

        expected_html = render_to_string('app/frame.html')

        self.assertEqual(actual_html, expected_html)

    def test_routing_response_from_signup_completed(self):
        """urlパス'/signup_completed'へのリクエストから'app/signup_completed.html'
        が返されることを確認する
        """
        url = '/signup_completed'
        username = 'test_user'
        password = 'valid_test_password'
        param_dict = {'username': username, 'password': '*' * len(password)}
        param_in_url = urlencode(param_dict)
        url_with_parameters = f'{url}?{param_in_url}'
        response = self.client.get(url_with_parameters)
        response_html = response.content.decode('utf8')

        self.assertIn('登録が完了しました', response_html)
        self.assertIn(username, response_html)

    def test_routing_response_from_pages(self):
        """urlパス'/pages'から返されるview関数にリクエストを送り
        app/pages.htmlを取得することを確認する
        """
        path = '/pages'
        actual_without_csrf = self.get_actual_html_with_user(path)

        expected_html = render_to_string('app/pages.html', request=get_request(path))
        expected_without_csrf = remove_csrf(expected_html)

        self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_routing_response_from_src_link(self):
        """urlパス'/src_link'から返されるview関数にリクエストを送り
        app/src_link.htmlを取得することを確認する
        """
        path = '/src_link'
        actual_without_csrf = self.get_actual_html_with_user(path)

        expected_without_csrf = self.get_expected_html(path)

        self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_routing_response_from_src_link_with_category(self):
        """urlパス'/src_link/?<clicked_category>'から返されるview関数に
        リクエストを送りapp/src_link.htmlを取得することを確認する
        """
        for category in CATEGORY_DICT.keys():
            with self.subTest(category=category):
                path = '/src_link/?'+category
                actual_without_csrf = self.get_actual_html_with_user_category(path, category)

                path_for_expected = '/src_link/' + category
                expected_without_csrf = self.get_expected_html(path_for_expected, category)

                self.assertEqual(actual_without_csrf, expected_without_csrf)

    def test_category_clear_request_clear_category_evals(self):
        """urlパス'/category_clear'へのリクエストが送られるとcategory_clear()が呼ばれ
        引数として渡されたカテゴリーの評価が消去されることを確認する
        """
        preference = Preference.objects.get(user=get_test_user())
        #IDの1から5までが'domestic'、6以降は別のカテゴリー
        domestic_good_ids = '1,2,3'
        other_good_ids = '6,10,15'
        domestic_uninterested_ids = '4,5'
        other_uninterested_ids = '11,12,16'
        preference.good_ids = domestic_good_ids + ',' + other_good_ids
        preference.uninterested_ids = domestic_uninterested_ids + ',' + other_uninterested_ids
        #評価以外のフィールドが消えないことを確認するために他のフィールドも用意する
        preference.good_noun_tfidf_pair = 'テスト,パス,リクエスト,フィールド'
        preference.uninterested_noun_tfidf_pair = '評価,消去,確認'
        preference.recommended_id_rate_pair = '6:0.500,7:0.450,8:0.400,9:0.350,10:0.300'
        preference.rejected_id_rate_pair = '10:0.600,9:0.550,8:0.500,7:0.450,6:0.400'
        preference.save()

        category = '国内'
        path = '/category_clear/' + category
        view = resolve(path)
        view.func(get_request_with_pref(path), category)
        
        preference = Preference.objects.get(user=get_test_user())
        result_good_ids = preference.good_ids.split(',')
        result_uninterested_ids = preference.uninterested_ids.split(',')
        #'国内'のカテゴリーの評価が消去されていることを確認
        for domestic_good_id in domestic_good_ids.split(','):
            self.assertNotIn(domestic_good_id, result_good_ids)
        for domestic_uninterested_id in domestic_uninterested_ids.split(','):
            self.assertNotIn(domestic_uninterested_id, result_uninterested_ids)
        #'国内'以外のカテゴリーの評価が消去されていないことを確認
        for other_good_id in other_good_ids.split(','):
            self.assertIn(other_good_id, preference.good_ids)
        for other_uninterested_id in other_uninterested_ids.split(','):
            self.assertIn(other_uninterested_id, preference.uninterested_ids)
        #評価以外のフィールドが消えないことを確認
        self.assertNotEqual(preference.good_noun_tfidf_pair, '')
        self.assertNotEqual(preference.uninterested_noun_tfidf_pair, '')
        self.assertNotEqual(preference.recommended_id_rate_pair, '')
        self.assertNotEqual(preference.rejected_id_rate_pair, '')

    def test_all_clear_request_clear_data(self):
        """urlパス'/all_clear'へのリクエストが送られるとall_clear()が呼ばれ
        全ての評価とそれに基づくPreferenceのフィールドが消去されることを確認する
        """
        preference = Preference.objects.get(user=get_test_user())
        preference.good_ids = '1,2,3'
        preference.uninterested_ids = '3,4,5'
        preference.good_noun_tfidf_pair = 'テスト,パス,リクエスト,フィールド'
        preference.uninterested_noun_tfidf_pair = '評価,消去,確認'
        preference.recommended_id_rate_pair = '6:0.500,7:0.450,8:0.400,9:0.350,10:0.300'
        preference.rejected_id_rate_pair = '10:0.600,9:0.550,8:0.500,7:0.450,6:0.400'
        preference.save()

        path = '/all_clear'
        view = resolve(path)
        view.func(get_request_with_pref(path))

        preference = Preference.objects.get(user=get_test_user())
        self.assertEqual(preference.good_ids, '')
        self.assertEqual(preference.uninterested_ids, '')
        self.assertEqual(preference.good_noun_tfidf_pair, '')
        self.assertEqual(preference.uninterested_noun_tfidf_pair, '')
        self.assertEqual(preference.recommended_id_rate_pair, '')
        self.assertEqual(preference.rejected_id_rate_pair, '')

    def test_eval_good_request_alter_model_field(self):
        """urlパス'/eval_good'へリクエストが送られると引数として渡した記事のIDが
        Preference.good_idsに追加され、二回めのリクエストでPreference.good_idsから
        除去されることを確認する
        """
        preference = Preference.objects.get(user=get_test_user())
        self.assertEqual(preference.good_ids, '')

        test_article = Article.objects.all()[0]
        path = '/eval_good/' + test_article.category + '/' + test_article.title
        data = {
            'clicked_category': test_article.category,
            'article_title': test_article.title
        }
        #'/eval_good'のリクエストで、引数として渡した記事のIDが
        #Preference.good_idsに追加されていることを確認
        self.client.post(path=path, data=data)

        preference = Preference.objects.get(user=get_test_user())
        self.assertIn(str(test_article.id), preference.good_ids)

        #二回目の'/eval_good'のリクエストで評価が消えることを確認
        self.client.post(path=path, data=data)

        preference = Preference.objects.get(user=get_test_user())
        self.assertNotIn(str(test_article.id), preference.good_ids)

    def test_eval_uninterested_request_alter_model_field(self):
        """urlパス'/eval_uninterested'へリクエストが送られると
        引数として渡した記事のIDがPreference.uninterested_idsに追加され、
        二回めのリクエストでPreference.uninterested_idsから除去されることを確認する
        """
        preference = Preference.objects.get(user=get_test_user())
        self.assertEqual(preference.uninterested_ids, '')

        test_article = Article.objects.all()[0]
        path = '/eval_uninterested/' + test_article.category + '/' + test_article.title
        data = {
            'clicked_category': test_article.category,
            'article_title': test_article.title
        }
        #'/eval_uninterested'のリクエストで、引数として渡した記事のIDが
        #Preference.uninterested_idsに追加されていることを確認
        self.client.post(path=path, data=data)

        preference = Preference.objects.get(user=get_test_user())
        self.assertIn(str(test_article.id), preference.uninterested_ids)

        #二回目の'/eval_uninterested'のリクエストで評価が消えることを確認
        self.client.post(path=path, data=data)

        preference = Preference.objects.get(user=get_test_user())
        self.assertNotIn(str(test_article.id), preference.uninterested_ids)

    def test_routing_loading_request_success(self):
        """urlパス'/loading'から返されるレスポンスが
        loading_circleを含んでいることを確認する
        """
        response = self.client.get('/loading')
        response_html = response.content.decode('utf8')
        self.assertEqual(response.status_code, REQUEST_OK)
        self.assertIn("loading_circle",response_html)

    def test_call_apply_choices_request_alter_preference(self):
        """urlパス'/call_apply_choices'へのリクエストがPreference内の
        good_noun_tfidf_pair、recommended_id_rate_pair、uninterested_nouns、
        rejected_id_rate_pairの値を算出し変更することを確認する
        """
        preference = Preference.objects.get(user=get_test_user())
        preference.good_ids = '1,2,3'
        preference.uninterested_ids = '3,4,5'
        preference.save()

        preference = Preference.objects.get(user=get_test_user())
        self.assertEqual(preference.good_noun_tfidf_pair, '')
        self.assertEqual(preference.uninterested_noun_tfidf_pair, '')
        self.assertEqual(preference.recommended_id_rate_pair, '')
        self.assertEqual(preference.rejected_id_rate_pair, '')

        path = '/call_apply_choices'
        view = resolve(path)
        view.func(get_request_with_pref(path))

        preference = Preference.objects.get(user=get_test_user())
        self.assertNotEqual(preference.good_noun_tfidf_pair, '')
        self.assertNotEqual(preference.uninterested_noun_tfidf_pair, '')
        self.assertNotEqual(preference.recommended_id_rate_pair, '')
        self.assertNotEqual(preference.rejected_id_rate_pair, '')

    def test_result_positive_request_returns_result_html(self):
        """good評価が0でない状態で'call_apply_choices'が呼ばれた後に
        urlパス'result_positive'へのリクエストが送られると'app/result.html'
        が返されて算出されたrateが表示されていることを確認する
        """
        #'/result_positive'が結果を表示するための用意
        preference = Preference.objects.get(user=get_test_user())
        preference.good_ids = '1,2,3'
        preference.save()
        path = '/call_apply_choices'
        view = resolve(path)
        view.func(get_request_with_pref(path))

        response = self.client.get('/result_positive')
        response_html = response.content.decode('utf8')
        self.assertEqual(response.status_code, REQUEST_OK)
        self.assertIn('「いいね」評価の記事から抽出', response_html)
        self.assertIn('<div class="result_rate">', response_html)
        self.assertIn('<a href=', response_html)

    def test_result_positive_request_returns_empty_result(self):
        """good評価からの一致率が算出されていない状態で
        urlパス'result_positive'へのリクエストが送られると'app/result.html'
        が返されて算出されたrateが表示されていないことを確認する
        """
        response = self.client.get('/result_positive')
        response_html = response.content.decode('utf8')
        self.assertEqual(response.status_code, REQUEST_OK)
        self.assertIn('「いいね」評価の記事から抽出', response_html)
        self.assertNotIn('<div class="result_rate">', response_html)
        self.assertNotIn('<a href=', response_html)

    def test_result_negative_request_returns_result_html(self):
        """uninterested評価が0でない状態で'call_apply_choices'が呼ばれた後に
        urlパス'result_negative'へのリクエストが送られると'app/result.html'
        が返されて算出されたrateが表示されていることを確認する
        """
        #'/result_negative'が結果を表示するための用意
        preference = Preference.objects.get(user=get_test_user())
        preference.uninterested_ids = '1,2,3'
        preference.save()
        path = '/call_apply_choices'
        view = resolve(path)
        view.func(get_request_with_pref(path))

        response = self.client.get('/result_negative')
        response_html = response.content.decode('utf8')
        self.assertEqual(response.status_code, REQUEST_OK)
        self.assertIn('「興味なし」評価の記事から抽出', response_html)
        self.assertIn('<div class="result_rate">', response_html)
        self.assertIn('<a href=', response_html)

    def test_result_negative_request_returns_empty_result(self):
        """uninterested評価からの一致率が算出されていない状態で
        urlパス'result_negative'へのリクエストが送られると'app/result.html'
        が返されて算出されたrateが表示されていないことを確認する
        """
        response = self.client.get('/result_negative')
        response_html = response.content.decode('utf8')
        self.assertEqual(response.status_code, REQUEST_OK)
        self.assertIn('「興味なし」評価の記事から抽出', response_html)
        self.assertNotIn('<div class="result_rate">', response_html)
        self.assertNotIn('<a href=', response_html)
    
    def get_actual_html_with_user_category(self, path, category):
        """pathから、カテゴリーを引数として受け取る関数とユーザー有りのリクエスト
        を取得しhtmlを読み込んで返すヘルパー関数
        """
        view = resolve(path)
        request = get_request(path)
        response = view.func(request, category)
        actual_html = response.content.decode('utf8')
        return remove_csrf(actual_html)

    def get_actual_html_with_user(self, path):
        """pathから関数とユーザー有りのリクエストを取得しhtmlを
        読み込んで返すヘルパー関数
        """
        view = resolve(path)
        request = get_request(path)
        response = view.func(request)
        actual_html = response.content.decode('utf8')
        return remove_csrf(actual_html)
    
    def get_expected_html(self, path, category='domestic'):
        """pathとcategoryから比較対象としてのhtmlを読み込んで返すヘルパー関数"""
        context={'category':category}
        expected_template = self.client.get(path, context)
        expected_html = expected_template.content.decode('utf8')
        return remove_csrf(expected_html)
