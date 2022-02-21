from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        opt = Options()
        opt.add_argument('--headless')
        opt.add_argument('--no-sandbox')
        self.browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', options=opt)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('https://www.google.com/')
        self.assertIn('Google', self.browser.title)
        # self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')

    