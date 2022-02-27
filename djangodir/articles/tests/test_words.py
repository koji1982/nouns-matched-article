from django.test import TestCase
from scraping.words import *

BASE_NOUNS = '名詞,一致,割合,算出,基準,リスト,コンマ,付属'
HALF_MATCH = '基準,リスト,名詞,半分,一致,残り,語句,相違'
UNMATCH_NOUNS = '全部,単語,意味,量,相違'


class WordsTest(TestCase):
    
    def test_extract_noun(self):
        """extract_noun()から返されるstrが、名詞と','を含んで
        それ以外が除去されていることを確認する
        """
        test_text = 'あからさまな名詞抽出テスト用のテキストです。'
        extracted_text = extract_noun(test_text)

        self.assertTrue('抽出' in extracted_text)
        self.assertTrue('テキスト' in extracted_text)
        self.assertTrue(',' in extracted_text)
        
        self.assertFalse('あからさまな' in extracted_text)
        self.assertFalse('の' in extracted_text)
        self.assertFalse('です。' in extracted_text)

    def test_extract_noun_with_empty_str_return_empty(self):
        empty_text = ''
        returned_text = extract_noun(empty_text)
        self.assertEqual(returned_text, empty_text)

    def test_extract_noun_with_none_raise_error(self):
        with self.assertRaises(AttributeError):
            extract_noun(None)

    def test_extract_noun_with_wrong_arg_raise_error(self):
        with self.assertRaises(TypeError):
            extract_noun(5)
        with self.assertRaises(TypeError):
            extract_noun(True)

    def test_extract_noun_without_arg_raise_error(self):
        with self.assertRaises(TypeError):
            extract_noun()

    def test_get_duplicate_rate(self):
        """get_duplicated_rate()が"""
        actual_duplicate_self = get_duplicate_rate(BASE_NOUNS, BASE_NOUNS)
        actual_half_match = get_duplicate_rate(BASE_NOUNS, HALF_MATCH)
        actual_unmatch  = get_duplicate_rate(BASE_NOUNS, UNMATCH_NOUNS)

        self.assertEqual(actual_duplicate_self, 1.0)
        self.assertEqual(actual_half_match, 0.5)
        self.assertEqual(actual_unmatch, 0.0)

    def test_get_duplicate_rate_with_one_side_empty_arg_return_zero(self):
        empty_text = ''
        empty_base = get_duplicate_rate(empty_text, BASE_NOUNS)
        base_empty = get_duplicate_rate(BASE_NOUNS, empty_text)
        self.assertEqual(empty_base, 0.0)
        self.assertEqual(base_empty, 0.0)

    def test_get_duplicate_rate_with_empty_matches_empty(self):
        empty_text = ''
        empty_empty = get_duplicate_rate(empty_text, empty_text)
        self.assertEqual(empty_empty, 1.0)

    def test_get_duplicate_rate_with_none_raise_error(self):
        with self.assertRaises(AttributeError):
            get_duplicate_rate(None, BASE_NOUNS)
        with self.assertRaises(AttributeError):
            get_duplicate_rate(BASE_NOUNS, None)

    def test_get_duplicate_rate_without_args(self):
        with self.assertRaises(TypeError):
            get_duplicate_rate()
        with self.assertRaises(TypeError):
            get_duplicate_rate(BASE_NOUNS)

    def test_get_duplicated_rate_with_wrong_args(self):
        with self.assertRaises(AttributeError):
            get_duplicate_rate(0.5, BASE_NOUNS)
        with self.assertRaises(AttributeError):
            get_duplicate_rate(BASE_NOUNS, True)


    def test_sort_duplicated_nouns_list(self):
        url_nouns_pair_list = [['http://half_match/', HALF_MATCH ], 
                               ['http://unmatch_nouns/', UNMATCH_NOUNS],
                               ['http://base_nouns/', BASE_NOUNS] ]
        self.assertEqual(url_nouns_pair_list[0][0], 'http://half_match/')
        self.assertEqual(url_nouns_pair_list[1][0], 'http://unmatch_nouns/')
        self.assertEqual(url_nouns_pair_list[2][0], 'http://base_nouns/')

        sorted_list = sort_duplicated_nouns_list(BASE_NOUNS, url_nouns_pair_list)

        print(sorted_list)
        print(sorted_list[0])
        print(sorted_list[1])
        print(sorted_list[2])

        self.assertEqual(sorted_list[0][0], 'http://base_nouns/')
        self.assertEqual(sorted_list[0][1], 1.0)
        self.assertEqual(sorted_list[1][0], 'http://half_match/')
        self.assertEqual(sorted_list[1][1], 0.5)
        self.assertEqual(sorted_list[2][0], 'http://unmatch_nouns/')
        self.assertEqual(sorted_list[2][1], 0.0)