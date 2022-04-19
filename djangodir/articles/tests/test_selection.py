from django.test import TestCase
from articles.selection import apply_choices
from articles.tests.helper import *

class SelectionTest(TestCase):

    fixtures = ['test_articles.json']

    def test_apply_choices_asign_preference_field(self):
        """apply_choices()が呼ばれることでPreferenceのフィールド
        good_nouns, recommended_id_rate_pair, uninterested_nouns,
        rejected_id_rate_pairの４つが作成、保存されることを確認する"""
        #Preference用意し、記事の評価を保存する
        prepare_user_pref(self)
        preference = Preference.objects.get(user=get_test_user())
        preference.good_ids = '1,2,3,4,5'
        preference.uninterested_ids = '6,7,8,9,10'
        preference.save()
        #各fieldが空であることを確認する
        self.assertEqual(preference.good_nouns, '')
        self.assertEqual(preference.uninterested_nouns, '')
        self.assertEqual(preference.recommended_id_rate_pair, '')
        self.assertEqual(preference.rejected_id_rate_pair, '')

        #テスト対象
        apply_choices(get_test_user())

        #各fieldが空でなくなっていることを確認する
        preference_after = Preference.objects.get(user=get_test_user())
        self.assertNotEqual(preference_after.good_nouns, '')
        self.assertNotEqual(preference_after.uninterested_nouns, '')
        self.assertNotEqual(preference_after.recommended_id_rate_pair, '')
        self.assertNotEqual(preference_after.rejected_id_rate_pair, '')

    def test_apply_choices_not_asign_field_without_evaluations(self):
        """apply_choices()が記事を未評価の状態で呼ばれた場合
        Preferenceのフィールドgood_nouns, recommended_id_rate_pair,
        uninterested_nouns,rejected_id_rate_pairの４つは
        作成されないことを確認する"""
        #Preference用意し、記事の評価を保存する
        prepare_user_pref(self)
        preference = Preference.objects.get(user=get_test_user())
        preference.good_ids = ''
        preference.uninterested_ids = ''
        preference.save()
        #各fieldが空であることを確認する
        self.assertEqual(preference.good_ids, '')
        self.assertEqual(preference.uninterested_ids, '')
        self.assertEqual(preference.good_nouns, '')
        self.assertEqual(preference.uninterested_nouns, '')
        self.assertEqual(preference.recommended_id_rate_pair, '')
        self.assertEqual(preference.rejected_id_rate_pair, '')

        #テスト対象
        apply_choices(get_test_user())

        #各fieldが空のままであることを確認する
        preference_after = Preference.objects.get(user=get_test_user())
        self.assertEqual(preference_after.good_ids, '')
        self.assertEqual(preference_after.uninterested_ids, '')
        self.assertEqual(preference_after.good_nouns, '')
        self.assertEqual(preference_after.uninterested_nouns, '')
        self.assertEqual(preference_after.recommended_id_rate_pair, '')
        self.assertEqual(preference_after.rejected_id_rate_pair, '')