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

    def test_tfidf_for_good(self):
        prepare_user_pref(self)
        preference = Preference.objects.get(user=get_test_user())
        preference.good_ids = '1,2,3,4,5'
        preference.uninterested_ids = '7,9,11,12,15'
        preference.save()
        
        compute_tfidf_cos_similarity(get_test_user())

    def test_make_merged_vectors_from_article_ids(self):

        text_1 = '今年,3,大阪,寝屋川,専門,学校,生,刃物,死亡,事件,強盗,致死,容疑,検察,官,送致,逆送,男,19,弁護,士,25,男,起訴,際,実名,報道,よう,大阪,記者,会見,小西,智子,弁護,士,親,虐待,こと,報復,の,玉野,まりこ,弁護,士,事件,の,人物,従属,立場,説明,結果,地域,出身,実名,報道,家族'
        text_2 = '岸田,文雄,首相,21,ニュージーランド,今年,3,大阪,寝屋川,専門,学校,生,アーダン,首相,官邸,会談,ロシア,ウクライナ,侵攻,非難,経済,制裁,対応,方針,一致,国,保障,防衛,分野,協力,強化,機密,情報,交換,情報,保護,協定,締結,交渉,開始,こと,確認,写真,G,20,ロシア,発言,米,欧,銀,トップ,途中,退席,鈴木,財務,相,同調,両氏,海洋,進出,中国,動向,念頭,東,南,シナ,海,地域,力,現状,変更,反対,認識,共有,インド,太平洋,実現,協力'
        text_3 = '静岡,銀行,愛知,名古屋,銀行,包括,業務,提携,こと,27,大筋,合意,同日,午後,発表,経営,資源,業務,効率,ほか,競争,中部,地方,存在,感,愛知,地盤,地方,銀行,愛知,銀行,中京,銀行,2022,10,経営,統合,基本,合意,静岡,銀,20,山梨,中央,銀行,包括,業務,提携,独立,ノウハウ,方向'
        text_4 = '社会,問題,インターネット,誹謗,ひぼう,中傷,抑止,侮辱,罪,厳罰,時代,変化,懲役,刑,禁錮,刑,拘禁,刑,一本化,刑法,関連,法,改正,案,21,衆院,会議,趣旨,説明,質疑,審議,図解,投稿,情報,開示,手続き,刑法,侮辱,罪,現行,法定,刑,拘留,科,料,改正,案,1,懲役,禁錮,30万,罰金,拘留,科,料,ネット,中傷,プロレスラー,木村,花,当時,22,命,問題,契機,厳罰,懲役,刑,禁錮,刑,廃止,受刑,特性,作業,指導,処遇,拘禁,刑,新設,1907,刑法,制定,刑,種類,名称,変更'
        text_5 = '自民党,保障,調査,会,会長,小野寺,五,典,防衛,相,21,会合,国家,保障,戦略,改定,提言,案,大筋,了承,図解,日本,弾,道,ミサイル,迎撃,体制,敵,基地,攻撃,イメージ,敵,基地,攻撃,能力,呼称,反撃,能力,保有,内容,専守防衛,維持,上,攻撃,対象,ミサイル,基地,指揮,統制,関連,機能,防衛,国,生産,GDP,比,2,念頭,5,増額,提言,案,敵,基地,攻撃,呼称,弾,道,ミサイル,攻撃,わが国,武力,攻撃,反撃,能力,保有,抑止,対処,呼称,反撃,能力,保有,具体,技術,力,向上,中国,北朝鮮,軍事,動向,迎撃,わが国,防衛,強調,車両,潜水,艦,ミサイル,発射,方式,攻撃,対象,基地,限定,もの,相手,国,指揮,統制,機能,等,明記'
        
        corpus = [text_1.replace(',', ' '),
                  text_2.replace(',', ' '),
                  text_3.replace(',', ' '),
                  text_4.replace(',', ' '),
                  text_5.replace(',', ' '),]
        vectorizer = TfidfVectorizer()
        tfidf_mat = vectorizer.fit_transform(corpus)
        cos_val = cosine_similarity(tfidf_mat.toarray())
        print(tfidf_mat.shape)
        print(tfidf_mat.toarray())

        tfidf_whole_id_list = [0, 1, 2, 3, 4]
        target_id_list = [0, 1]

        merged_vectors = make_merged_vectors_from_article_ids(tfidf_mat,
                                                              tfidf_whole_id_list,
                                                              target_id_list)
        print(len(merged_vectors[0]))
        print(merged_vectors)

        uneval_id_list = [2, 3]
        uneval_vectors = extract_vectors_from_article_ids(tfidf_mat,
                                                          tfidf_whole_id_list,
                                                          uneval_id_list )

        print(len(uneval_vectors[1]))
        print(uneval_vectors)

        result = cosine_similarity(merged_vectors, uneval_vectors)
        print(len(result))
        print(result)
    
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