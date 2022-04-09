from django.test import TestCase
from articles.models import Article, Preference
from articles.tests.helper import *
from articles.templatetags.external_functions import apply_choices

class ModelsTest(TestCase):

    fixtures = ["test_articles.json"]

    def setUp(self):
        self.prepare_user_pref()

    def tearDown(self):
        self.client.logout()

    #Articleのテスト
    def test_article_str_returns_title(self):
        """Articleをstr()に渡した時にtitleの文字列を返すことを確認する"""
        article = Article.objects.all()[0]
        self.assertEqual(str(article), article.title)

    def test_article_get_id_returns_str_id(self):
        """get_id()がArticle.idをstr型で返すことを確認する"""
        article = Article.objects.all()[0]
        self.assertEqual(article.get_id(), str(article.id))

    #Preferenceのテスト
    def test_preference_get_good_list_returns_good_ids_by_list(self):
        """get_good_list()がgood_idsをlist型にして返すことを確認する"""
        preference = Preference.objects.get(username=get_test_user())
        self.assertEqual(preference.good_ids, '')
        self.assertEqual(preference.get_good_list(), [])
        test_eval_str = '1,2,3,4,5'
        preference.good_ids = test_eval_str
        preference.save()

        self.assertEqual(preference.good_ids, test_eval_str)
        self.assertEqual(preference.get_good_list(), test_eval_str.split(','))

    def test_preference_get_uninterested_list_returns_uninterested_ids_by_list(self):
        """get_uninterested_list()がuninterested_idsをlist型にして返すことを確認する"""
        preference = Preference.objects.get(username=get_test_user())
        self.assertEqual(preference.uninterested_ids, '')
        self.assertEqual(preference.get_uninterested_list(), [])
        test_eval_str = '1,2,3,4,5'
        preference.uninterested_ids = test_eval_str
        preference.save()

        self.assertEqual(preference.uninterested_ids, test_eval_str)
        self.assertEqual(preference.get_uninterested_list(), test_eval_str.split(','))

    def test_evaluate_good_put_arg_article_id_in_good_ids(self):
        """evaluate_good()が引数として受け取った記事IDを
        good_idsに追加することを確認する
        """
        test_evaluated_id = '5'
        preference = Preference.objects.get(username=get_test_user())
        self.assertNotIn(test_evaluated_id, preference.get_good_list())

        preference.evaluate_good(test_evaluated_id)

        self.assertIn(test_evaluated_id, preference.get_good_list())
        
    def test_evaluate_good_remove_arg_id_same_id_already_exists(self):
        """evaluate_good()が引数として受け取った記事IDが既にgood_ids内にある場合は
        そのIDをgood_idsから除去することを確認する
        """
        preference = Preference.objects.get(username=get_test_user())
        preference.good_ids = '1,2,3,4,5'
        preference.save()

        test_evaluated_id = '5'
        self.assertIn(test_evaluated_id, preference.get_good_list())

        preference.evaluate_good(test_evaluated_id)

        self.assertNotIn(test_evaluated_id, preference.get_good_list())

    def test_evaluate_good_remove_arg_id_same_uninterested_id(self):
        """evaluate_good()が引数として受け取った記事IDがuninterested_ids内にある場合は
        そのIDをuninterested_idsから除去することを確認する
        """
        preference = Preference.objects.get(username=get_test_user())
        preference.uninterested_ids = '1,2,3,4,5'
        preference.save()

        test_evaluated_id = '5'
        self.assertIn(test_evaluated_id, preference.get_uninterested_list())

        preference.evaluate_good(test_evaluated_id)

        self.assertNotIn(test_evaluated_id, preference.get_uninterested_list())

    def test_evaluate_uninterest_arg_id_put_uninterested_ids(self):
        """evaluate_uninterest()が引数として受け取ったIDを
        uninterested_idsに追加することを確認する
        """
        test_evaluated_id = '5'
        preference = Preference.objects.get(username=get_test_user())
        self.assertNotIn(test_evaluated_id, preference.get_uninterested_list())

        preference.evaluate_uninterest(test_evaluated_id)

        self.assertIn(test_evaluated_id, preference.get_uninterested_list())

    def test_evaluate_uninterest_remove_arg_id_same_id_already_exists(self):
        """evaluate_uninterest()が引数として受け取った記事IDが既にuninterested_ids内にある場合は
        そのIDをuninterested_idsから除去することを確認する
        """
        preference = Preference.objects.get(username=get_test_user())
        preference.uninterested_ids = '1,2,3,4,5'
        preference.save()

        test_evaluated_id = '5'
        self.assertIn(test_evaluated_id, preference.get_uninterested_list())

        preference.evaluate_uninterest(test_evaluated_id)

        self.assertNotIn(test_evaluated_id, preference.get_uninterested_list())

    def test_evaluate_uninterest_remove_arg_id_same_good_id(self):
        """evaluate_uninterest()が引数として受け取った記事IDがgood_ids内にある場合は
        そのIDをgood_idsから除去することを確認する
        """
        preference = Preference.objects.get(username=get_test_user())
        preference.good_ids = '1,2,3,4,5'
        preference.save()

        test_evaluated_id = '5'
        self.assertIn(test_evaluated_id, preference.get_good_list())

        preference.evaluate_uninterest(test_evaluated_id)

        self.assertNotIn(test_evaluated_id, preference.get_good_list())

    def test_category_clear_remove_evaluation_in_arg_category(self):
        """category_clear()が引数で指定したcategoryの評価を消去することを確認する"""
        target_category = 'world'
        preference = Preference.objects.get(username=get_test_user())
        articles = Article.objects.all()
        article_ids = []
        target_category_ids = []
        for article in articles:
            article_ids.append(article.get_id())
            if article.category == target_category:
                target_category_ids.append(article.get_id())
        
        #good_ids側をテスト
        preference.good_ids = ','.join(article_ids)
        preference.save()
        good_id_list = preference.get_good_list()
        for target_category_id in target_category_ids:
            with self.subTest(target_category_id=target_category_id):
                self.assertIn(target_category_id, good_id_list)
        
        preference.category_clear(target_category)

        good_id_list = preference.get_good_list()
        for target_category_id in target_category_ids:
            with self.subTest(target_category_id=target_category_id):
                self.assertNotIn(target_category_id, good_id_list)
        
        #uninterested_ids側をテスト
        preference.uninterested_ids = ','.join(article_ids)
        preference.save()
        uninterested_id_list = preference.get_uninterested_list()
        for target_category_id in target_category_ids:
            with self.subTest(target_category_id=target_category_id):
                self.assertIn(target_category_id, uninterested_id_list)
        
        preference.category_clear(target_category)

        uninterested_id_list = preference.get_uninterested_list()
        for target_category_id in target_category_ids:
            with self.subTest(target_category_id=target_category_id):
                self.assertNotIn(target_category_id, uninterested_id_list)
        
    def test_category_clear_not_remove_with_wrong_category(self):
        """category_clear()が引数で誤ったcategoryが渡された時に、
        評価IDリストが変化しないことを確認する"""
        target_category = 'wrong_category'
        preference = Preference.objects.get(username=get_test_user())
        articles = Article.objects.all()
        article_ids = []
        for article in articles:
            article_ids.append(article.get_id())
        
        #good_ids側をテスト
        preference.good_ids = ','.join(article_ids)
        preference.save()
        good_id_list = preference.get_good_list()
        self.assertListEqual(good_id_list, article_ids)
        
        preference.category_clear(target_category)

        good_id_list = preference.get_good_list()
        self.assertListEqual(good_id_list, article_ids)
        
        #uninterested_ids側をテスト
        preference.uninterested_ids = ','.join(article_ids)
        preference.save()
        uninterested_id_list = preference.get_uninterested_list()
        self.assertListEqual(uninterested_id_list, article_ids)
        
        preference.category_clear(target_category)

        uninterested_id_list = preference.get_uninterested_list()
        self.assertListEqual(uninterested_id_list, article_ids)

    def test_all_clear_remove_all_evaluations(self):
        """all_clear()が全ての評価を消去することを確認する"""
        preference = Preference.objects.get(username=get_test_user())
        articles = Article.objects.all()
        article_ids = []
        for article in articles:
            article_ids.append(article.get_id())

        #good_ids側をテスト
        preference.good_ids = ','.join(article_ids)
        preference.save()
        good_id_list = preference.get_good_list()
        self.assertListEqual(good_id_list, article_ids)
        
        preference.all_clear()

        good_id_list = preference.get_good_list()
        self.assertListEqual(good_id_list, [])
        
        #uninterested_ids側をテスト
        preference.uninterested_ids = ','.join(article_ids)
        preference.save()
        uninterested_id_list = preference.get_uninterested_list()
        self.assertListEqual(uninterested_id_list, article_ids)
        
        preference.all_clear()

        uninterested_id_list = preference.get_uninterested_list()
        self.assertListEqual(uninterested_id_list, [])

    def test_get_recommended_id_rate_dict_get_id_rate_dict(self):
        """get_recommended_id_rate_dict()が辞書{id:rate}を返すことを確認する"""
        preference = Preference.objects.get(username=get_test_user())
        preference.good_ids = '1,2,3,4,5'
        preference.save()
        previous_dict = preference.get_recommended_id_rate_dict()
        self.assertEqual(len(previous_dict), 0)
        request = get_request('/call_apply_choices')
        request.user = get_test_user()
        apply_choices(request)

        preference = Preference.objects.get(username=get_test_user())
        result_dict = preference.get_recommended_id_rate_dict()
        
        self.assertNotEqual(len(result_dict), 0)

    def test_get_recommended_id_rate_dict_get_empty_without_calc(self):
        """apply_choices()が事前に呼ばれていない場合、
        get_recommended_id_rate_dict()が空の辞書を返すことを確認する
        """
        preference = Preference.objects.get(username=get_test_user())
        articles = Article.objects.all()
        article_ids = []
        for article in articles:
            article_ids.append(article.get_id())
        preference.good_ids = ','.join(article_ids)
        preference.save()
        good_id_list = preference.get_good_list()
        self.assertListEqual(good_id_list, article_ids)

        result_dict = preference.get_recommended_id_rate_dict()

        self.assertDictEqual(result_dict, {})

    def test_get_recommended_id_rate_dict_get_empty_with_unevaluated(self):
        """good_idsが空の時、get_recommended_id_rate_dict()が空の辞書を返すことを確認する"""
        preference = Preference.objects.get(username=get_test_user())
        self.assertEqual(preference.good_ids, '')
        apply_choices(get_request('/call_apply_choices'))

        result_dict = preference.get_recommended_id_rate_dict()

        self.assertDictEqual(result_dict, {})

    def test_save_recommended_id_rate_dict_save_key_values(self):
        """save_recommended_id_rate_dict()が辞書型の引数をstrで保存することを確認する"""
        preference = Preference.objects.get(username=get_test_user())
        self.assertEqual(preference.recommended_id_rate_pair, '')

        test_data = {
            '6':'0.375',
            '7':'0.375',
            '8':'0.375',
            '9':'0.375',
            '10':'0.375',
        }
        preference.save_recommended_id_rate_dict(test_data)

        self.assertNotEqual(preference.recommended_id_rate_pair, '')

    def test_get_rejected_id_rate_dict_get_id_rate_dict(self):
        """get_rejected_id_rate_dict()が辞書{id:rate}を返すことを確認する"""
        preference = Preference.objects.get(username=get_test_user())
        preference.uninterested_ids = '1,2,3,4,5'
        preference.save()
        previous_dict = preference.get_rejected_id_rate_dict()
        self.assertEqual(len(previous_dict), 0)
        request = get_request('/call_apply_choices')
        request.user = get_test_user()
        apply_choices(request)

        preference = Preference.objects.get(username=get_test_user())
        result_dict = preference.get_rejected_id_rate_dict()
        
        self.assertNotEqual(len(result_dict), 0)

    def test_get_rejected_id_rate_dict_get_empty_without_calc(self):
        """apply_choices()が事前に呼ばれていない場合、
        get_rejected_id_rate_dict()が空の辞書を返すことを確認する"""
        preference = Preference.objects.get(username=get_test_user())
        articles = Article.objects.all()
        article_ids = []
        for article in articles:
            article_ids.append(article.get_id())
        preference.uninterested_ids = ','.join(article_ids)
        preference.save()
        uninterested_id_list = preference.get_uninterested_list()
        self.assertListEqual(uninterested_id_list, article_ids)

        result_dict = preference.get_rejected_id_rate_dict()

        self.assertDictEqual(result_dict, {})

    def test_get_rejected_id_rate_dict_get_empty_with_unevaluated(self):
        """uninterested_idsが空の時、
        get_rejected_id_rate_dict()が空の辞書を返すことを確認する
        """
        preference = Preference.objects.get(username=get_test_user())
        self.assertEqual(preference.uninterested_ids, '')
        apply_choices(get_request('/call_apply_choices'))

        result_dict = preference.get_rejected_id_rate_dict()

        self.assertDictEqual(result_dict, {})

    def test_save_rejected_id_rate_dict_save_key_values(self):
        """seva_rejected_id_rate_dict()が辞書型の引数をstrで保存することを確認する"""
        preference = Preference.objects.get(username=get_test_user())
        self.assertEqual(preference.rejected_id_rate_pair, '')

        test_data = {
            '6':'0.375',
            '7':'0.375',
            '8':'0.375',
            '9':'0.375',
            '10':'0.375',
        }
        preference.save_rejected_id_rate_dict(test_data)

        self.assertNotEqual(preference.rejected_id_rate_pair, '')

    def test_convert_dict_to_str(self):
        """convert_dict_to_str()が"""
        preference = Preference.objects.get(username=get_test_user())
        test_data = {
            '6':'0.375',
            '7':'0.375',
            '8':'0.375',
        }

        actual = preference.convert_dict_to_str(test_data)

        expected = ''
        for key, val in test_data.items():
            additions = key + ':' + val + ','
            expected += additions
        #最後の','だけ除去する
        expected = expected[:-1]

        self.assertEqual(actual, expected)

    def test_convert_str_to_dict(self):
        """convert_str_to_dict()が辞書型に合わせて書かれたstrを
        dictに変換することを確認する
        """
        preference = Preference.objects.get(username=get_test_user())
        test_data_str = '6:0.375,7:0.375,8:0.375'

        actual = preference.convert_str_to_dict(test_data_str)

        item_list = test_data_str.split(',')
        expected = {}
        for element in item_list:
            key_val = element.split(':')
            expected[key_val[0]] = key_val[1]

        self.assertEqual(actual, expected)

    #Userのテスト
    def test_str_get_username(self):
        """Userオブジェクトをstr()に渡した時にusernameの文字列を返すことを確認する"""
        user = User.objects.get(username=get_test_user())
        self.assertEqual(str(user), user.username)

    #ヘルパー関数
    def prepare_user_pref(self):
        user = get_test_user()
        self.client.force_login(user)
        create_test_preference(user)