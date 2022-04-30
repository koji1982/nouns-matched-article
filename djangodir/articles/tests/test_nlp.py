from pydoc import Helper
from unittest.mock import MagicMock
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.test import TestCase
from articles.nlp import *
from articles.tests.helper import *

BASE_NOUNS = '名詞,一致,割合,算出,基準,リスト,コンマ,付属'
HALF_MATCH = '基準,リスト,名詞,半分,一致,残り,語句,相違'
UNMATCH_NOUNS = '全部,単語,意味,量,相違'


class NlpTest(TestCase):

    fixtures = ['test_articles.json']

    def test_compute_tfidf_cos_similarity(self):
        prepare_user_pref(self)
        preference = Preference.objects.get(user=get_test_user())
        preference.good_ids = '1,2,3,4,5'
        preference.uninterested_ids = '7,9,11,12,15'
        preference.save()

        self.assertEqual(preference.good_noun_tfidf_pair, '')
        self.assertEqual(preference.uninterested_noun_tfidf_pair, '')
        self.assertEqual(preference.recommended_id_rate_pair, '')
        self.assertEqual(preference.rejected_id_rate_pair, '')
        
        compute_tfidf_cos_similarity(get_test_user())

        preference = Preference.objects.get(user=get_test_user())
        self.assertNotEqual(preference.good_noun_tfidf_pair, '')
        self.assertNotEqual(preference.uninterested_noun_tfidf_pair, '')
        self.assertNotEqual(preference.recommended_id_rate_pair, '')
        self.assertNotEqual(preference.rejected_id_rate_pair, '')
    
    def test_extract_noun(self):
        """extract_noun()から返されるstrが、名詞と','を含んで
        それ以外が除去されていることを確認する
        """
        test_text = 'あからさまな名詞抽出テスト用のテキストです。'
        actual_extracted = extract_noun(test_text)

        expected_true = ['抽出', 'テキスト', ',']
        expected_false = ['あからさまな', 'の', 'です', '。']

        for word in expected_true:
            with self.subTest(expected_contains=expected_true):
                self.assertTrue(word in actual_extracted)
        
        for word in expected_false:
            with self.subTest(unexpected_contains=expected_false):
                self.assertFalse(word in actual_extracted)

    def test_extract_noun_with_empty_str_return_empty(self):
        """extract_noun()に空のstrを渡した場合は空のstrが返ってくる"""
        empty_text = ''
        returned_text = extract_noun(empty_text)
        self.assertEqual(returned_text, empty_text)

    def test_extract_noun_with_none(self):
        """extract_noun()にNoneを渡した場合はErrorを送出する"""
        with self.assertRaises(AttributeError):
            extract_noun(None)

    def test_extract_noun_with_wrong_arg(self):
        """extract_noun()にstr以外の型を渡した場合はErrorを送出する"""
        except_str_args = [5, 0.2, True, list()]
        for arg in except_str_args:
            with self.subTest(arg=arg):
                with self.assertRaises(TypeError):
                    extract_noun(arg)

    def test_extract_noun_without_arg(self):
        """extract_noun()を引数無しで呼び出した場合はErrorを送出する"""
        with self.assertRaises(TypeError):
            extract_noun()

    def test_get_duplicate_rate(self):
        """get_duplicated_rate()が、第一引数に対して第二引数の単語がどれだけ重複しているか
        の割合を返すことを確認する
        """
        #全ての単語が同じ場合は1.0を返し、全く一致しない場合は0.0を返す
        words_match_rate_pair = {BASE_NOUNS:1.0, HALF_MATCH:0.5, UNMATCH_NOUNS:0.0}
        for words, expected_rate in words_match_rate_pair.items():
            with self.subTest(words=words, expected_rate=expected_rate):
                actual_rate = get_duplicate_rate(BASE_NOUNS, words)
                self.assertEqual(actual_rate, expected_rate)

    def test_get_duplicate_rate_with_one_side_empty_arg_return_zero(self):
        """get_duplicate_rate()のどちらか片方の引数が空の文字列の場合は0.0を返す"""
        empty_text = ''
        empty_base = get_duplicate_rate(empty_text, BASE_NOUNS)
        base_empty = get_duplicate_rate(BASE_NOUNS, empty_text)
        self.assertEqual(empty_base, 0.0)
        self.assertEqual(base_empty, 0.0)

    def test_get_duplicate_rate_with_empty_matches_empty(self):
        """get_duplicate_rate()の引数がどちらも空の文字列の場合は1.0を返す"""
        empty_text = ''
        empty_empty = get_duplicate_rate(empty_text, empty_text)
        self.assertEqual(empty_empty, 1.0)

    def test_get_duplicate_rate_with_none(self):
        """get_duplicate_rate()にNoneを渡した場合はErrorを送出する"""
        with self.assertRaises(AttributeError):
            get_duplicate_rate(None, BASE_NOUNS)
        with self.assertRaises(AttributeError):
            get_duplicate_rate(BASE_NOUNS, None)

    def test_get_duplicate_rate_without_args(self):
        """get_duplicate_rate()に渡す引数が足りない場合はErrorを送出する"""
        with self.assertRaises(TypeError):
            get_duplicate_rate()
        with self.assertRaises(TypeError):
            get_duplicate_rate(source=BASE_NOUNS)
        with self.assertRaises(TypeError):
            get_duplicate_rate(target=BASE_NOUNS)

    def test_get_duplicated_rate_with_wrong_args(self):
        """get_duplicate_rate()にstr以外の型を引数として渡すとErrorを送出する"""
        except_str_args = [7, 0.5, True, tuple()]
        for arg in except_str_args:
            with self.subTest(arg=arg):
                with self.assertRaises(AttributeError):
                    get_duplicate_rate(arg, BASE_NOUNS)
                with self.assertRaises(AttributeError):
                    get_duplicate_rate(BASE_NOUNS, arg)

    def test_make_matched_rate_dict(self):
        """make_matched_rate_dict()が第一引数を基準にした一致率で、
        第二引数の一致率を算出して{id:rate}の辞書の形で返すことを確認する
        """
        id_nouns_pair_list = {'1':HALF_MATCH, 
                              '2':UNMATCH_NOUNS,
                              '3':BASE_NOUNS}

        matched_rate_dict = make_matched_rate_dict(BASE_NOUNS, id_nouns_pair_list)

        self.assertEqual(matched_rate_dict['1'], '0.5')
        self.assertEqual(matched_rate_dict['2'], '0.0')
        self.assertEqual(matched_rate_dict['3'], '1.0')

    def test_make_matched_rate_dict_with_unexpected_args(self):
        """make_matched_rate_dict()に対して第一引数str,第二引数dict{str:str}
        以外の型が渡された場合にはErrorを送出する
        """
        correct_first_arg = BASE_NOUNS
        correct_second_arg = {'1':HALF_MATCH, 
                              '2':UNMATCH_NOUNS,
                              '3':BASE_NOUNS}
        list_as_wrong_arg = BASE_NOUNS
        wrong_key_second = { 1:HALF_MATCH,
                             2:UNMATCH_NOUNS,
                             3:BASE_NOUNS}
        wrong_val_second1 = { '1':['名詞','一致','割合','算出','基準','リスト','コンマ','付属'],
                             '2':['基準','リスト','名詞','半分','一致','残り','語句','相違'],
                             '3':['全部','単語','意味','量','相違']}
        wrong_val_second2 = {'1': 'wrong_value_1',
                             '2': 'wrong_value_2',
                             '3': 'wrong_value_3'}
        with self.assertRaises(TypeError):
            make_matched_rate_dict('wrong_first_arg', correct_second_arg)
        with self.assertRaises(TypeError):
            make_matched_rate_dict(correct_first_arg, wrong_key_second)
        with self.assertRaises(TypeError):
            make_matched_rate_dict(correct_first_arg, wrong_val_second1)
        with self.assertRaises(TypeError):
            make_matched_rate_dict(correct_first_arg, wrong_val_second2)
        with self.assertRaises(TypeError):
            make_matched_rate_dict(7, correct_second_arg)
        with self.assertRaises(AttributeError):
            make_matched_rate_dict(correct_first_arg, 0.5)
        with self.assertRaises(AttributeError):
            make_matched_rate_dict(correct_first_arg, list_as_wrong_arg)
        
    def test_make_matched_rate_dict_with_empty_args(self):
        """make_matched_rate_dict()に渡す引数が足りない場合はErrorを送出する"""
        correct_first_arg = BASE_NOUNS
        correct_second_arg = {'1':HALF_MATCH, 
                              '2':UNMATCH_NOUNS,
                              '3':BASE_NOUNS}
        with self.assertRaises(TypeError):
            make_matched_rate_dict(url_nouns_pair_list=correct_second_arg)
        with self.assertRaises(TypeError):
            make_matched_rate_dict(base_nouns=correct_first_arg)
        with self.assertRaises(TypeError):
            make_matched_rate_dict()

    def test_make_matched_rate_dict_returns_empty_dict_with_empty_str(self):
        """make_matched_rate_dict()の第一引数が空のstr '' だった場合
        空のdictを返す
        """
        correct_second_arg = {'1':HALF_MATCH, 
                              '2':UNMATCH_NOUNS,
                              '3':BASE_NOUNS}
        self.assertDictEqual(make_matched_rate_dict('',correct_second_arg), {})