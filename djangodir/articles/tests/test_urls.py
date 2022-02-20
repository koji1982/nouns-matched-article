import time
import unittest
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from django.test import TestCase
from django.urls import resolve
from django.shortcuts import render
from django.http import HttpRequest
from django.template.loader import render_to_string
from articles.views import article_response
from articles.models import Article

class UrlTests(TestCase):
    fixtures = ["test_articles.json"]

    article_response = None

    def test_for_ci(self):
        self.assertEqual(1+1, 2)

    def test_webdriver(self):
        opt = Options()
        opt.add_argument('--headless')
        opt.add_argument('--no-sandbox')
        browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=opt)
        browser.get('https://www.google.com/')
        self.assertTrue( ('Google' in browser.title) )

    def setUp(self):
        opt = Options()
        opt.add_argument('--headless')
        opt.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=opt)
        # Article.objects.create(url='dummy', category='domestic',
        #                        date='dummy', title='dummy_title',
        #                        body='dummy', noun=['dummy'])

    def tearDown(self):
        self.browser.quit()
        print('tearDown')

    def test_url_resolve(self):
        found = resolve('/')
        self.assertEqual(found.func, article_response)

    def test_return_correct_html(self):
        request = HttpRequest()
        response = article_response(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Frame Test</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_visitor_test(self):
        self.browser.get('http://web:80/')
        right_frame = self.browser.find_element_by_name("right_frame")
        print(right_frame.get_attribute(name="src"))
        self.browser.switch_to_frame(right_frame)
        input_box = self.browser.find_elements_by_tag_name("p")
        for element in input_box:
            print(element.text)
        self.assertIn('Frame Test', self.browser.title)

    def test_render_html(self):
        request = HttpRequest()
        response = article_response(request)
        html = response.content.decode('utf8')
        expected_html = render_to_string('app/frame.html')
        self.assertEqual(html, expected_html)

    def test_return_html(self):
        print('client.get')
        response = self.client.get('/')
        print('response.content.decode')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Frame Test</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'app/frame.html')

    def test_template_file(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'app/frame.html')

    def test_saving_and_retrieving_Articles(self):

        for element in Article.objects.all():
            print(element.title)

        dummy_article_1 =Article.objects.create(url='dummy_url_1', category='domestic',
                                                date='dummy', title='dummy_title_1',
                                                body='dummy_1', noun=['dummy_1'])
        dummy_article_1.save()

        dummy_article_2 = Article.objects.create(url='dummy_url_2', category='domestic',
                                                 date='dummy', title='dummy_title_2',
                                                 body='dummy_2', noun=['dummy_2'])
        dummy_article_2.save()

        self.assertEqual(Article.objects.count(), 7)

        saved_items = Article.objects.all()
        first_saved_article = saved_items[0]
        second_saved_article = saved_items[1]
        self.assertEqual(first_saved_article.url, 'http://dummy_url_1/')
        self.assertEqual(second_saved_article.url, 'http://dummy_url_2/')

        response = self.client.post('/src_link.html', data={'records': saved_items })
        self.assertIn(saved_items[0].title, response.content.decode())

        html_text = BeautifulSoup(response.content.decode(), 'html.parser')
        test_table_td = html_text.select('#test_table td')
        found_test_table = html_text.find(id='test_table')
        for select in test_table_td:
            print(select.get_text(strip=True))
        print(found_test_table.get_text(strip=True))

        print('start browser loading')
        self.browser.get('http://web:80/')
        self.browser.refresh()
        right_frame = self.browser.find_element_by_name("right_frame")
        self.browser.switch_to_frame(right_frame)
        # self.wait_for_loaded('dummy', 'test_table', 'tr')
        # test_table = self.browser.find_element_by_id('test_table')
        records = self.browser.find_elements_by_tag_name('a')
        #他のリンクが表示されていて、データベース内が表示されないので→渡し方を検討する
        #テストデータだけ取得出来てない
        self.assertTrue(any(record.text == '国内' for record in records))
        # print(records.count())
        for record in records:
            print(record.text)
        print('record check finished')

        # self.assertIn('element_from_views', [record.text for record in records])

    def test_database_is_empty(self):
        self.client.get('/src_link.html')
        self.assertEqual(Article.objects.count(), 5)

    MAX_WAIT = 10

    def wait_for_loaded(self, expected_text, target_id, target_tag):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id(target_id)
                target = table.find_elements_by_tag_name(target_tag)
                self.assertIn(expected_text, [actual.text for actual in target])
                return
            except (AssertionError, WebDriverException, NoSuchElementException) as e:
                if time.time() - start_time > self.MAX_WAIT:
                    raise e
                time.sleep(0.5)
