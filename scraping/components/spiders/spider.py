import requests
import re
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from unicodedata import category
from ..items import ArticleItem


class ArticleSpider(CrawlSpider):
    name = 'article_spider'
    allowed_domains = ['www.yahoo.co.jp', 'news.yahoo.co.jp']
    start_urls = [
        'https://news.yahoo.co.jp/topics/domestic?page=1',
        # 'https://news.yahoo.co.jp/topics/world?page=1',
        # 'https://news.yahoo.co.jp/topics/business?page=1',
        # 'https://news.yahoo.co.jp/topics/entertainment?page=1',
        # 'https://news.yahoo.co.jp/topics/sports?page=1',
        # 'https://news.yahoo.co.jp/topics/it?page=1',
        # 'https://news.yahoo.co.jp/topics/science?page=1',
        # 'https://news.yahoo.co.jp/topics/local?page=1'
    ]

    rules = [
        Rule(LinkExtractor(r'https://news.yahoo.co.jp/topics/domestic'), callback='parse_newsfeed', follow=True),
        Rule(LinkExtractor(r'https://news.yahoo.co.jp/topics/world'), callback='parse_newsfeed', follow=True),
        Rule(LinkExtractor(r'https://news.yahoo.co.jp/topics/business'), callback='parse_newsfeed', follow=True),
        Rule(LinkExtractor(r'https://news.yahoo.co.jp/topics/entertainment'), callback='parse_newsfeed', follow=True),
        Rule(LinkExtractor(r'https://news.yahoo.co.jp/topics/sports'), callback='parse_newsfeed', follow=True),
        Rule(LinkExtractor(r'https://news.yahoo.co.jp/topics/it'), callback='parse_newsfeed', follow=True),
        Rule(LinkExtractor(r'https://news.yahoo.co.jp/topics/science'), callback='parse_newsfeed', follow=True),
        Rule(LinkExtractor(r'https://news.yahoo.co.jp/topics/local'), callback='parse_newsfeed', follow=True)
    ]

    categories = {
        'domestic', 'world', 'business', 'entertainment',
        'sports', 'it', 'science', 'local'
    }

    def parse_newsfeed(self, response):
        #ニュースカテゴリーごとに呼ばれる関数なのでここでカテゴリーを格納しておく
        url = response.url
        current_category = None
        url_tail = url.split("/")[-1]
        print(url_tail)
        for category in self.categories:
            if re.match(category, url_tail) is not None:
                current_category = category
                break
        #記事リストからリンクを取り出し、各リンクを辿る
        htmllinks = response.css('a.newsFeed_item_link::attr(href)').getall()
        newsSummaryUrls = [link for link in htmllinks if 'pickup' in link]
        for newsSummaryUrl in newsSummaryUrls:
            #導入ページを経由して記事本文を取り出す
            newsSummaryResponse = requests.get(newsSummaryUrl)
            newsSummaryHtml = BeautifulSoup(newsSummaryResponse.text, 'html.parser')
            articleLinkTag = newsSummaryHtml.find('a', text=['記事全文を読む', '続きを読む'])
            if articleLinkTag is None:
                continue
            articleUrl = articleLinkTag.get('href')
            articleResponse = requests.get(articleUrl)
            articleHtml = BeautifulSoup(articleResponse.text, 'html.parser')
            articleBodyTag = articleHtml.find('p', class_='highLightSearchTarget')
            if articleBodyTag is None:
                continue
            yield ArticleItem(
                url=articleUrl,
                category=current_category,
                date=articleHtml.time.get_text(),
                title=articleHtml.title.get_text(),
                body=articleBodyTag.get_text()
                )