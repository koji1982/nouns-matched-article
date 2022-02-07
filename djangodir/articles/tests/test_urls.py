from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class UrlTests(TestCase):
    def test_for_ci(self):
        self.assertEqual(1+1, 2)

    def test_webdriver(self):
        opt = Options()
        opt.add_argument('--headless')
        opt.add_argument('--no-sandbox')
        browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=opt)
        browser.get('https://www.google.com/')
        self.assertTrue( ('Google' in browser.title) )
