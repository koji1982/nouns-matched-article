from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ArticleItem
import requests
from bs4 import BeautifulSoup


class ArticleSpider(CrawlSpider):
    name = 'article_spider'
    allowed_domains = ['www.yahoo.co.jp', 'news.yahoo.co.jp']
    start_urls = ['https://news.yahoo.co.jp/topics/domestic?page=1']

    rules = [
        Rule(LinkExtractor(r'https://news.yahoo.co.jp/topics/domestic\?page'), callback='parse_newsfeed', follow=True),
    ]

    def parse_newsfeed(self, response):
        htmllinks = response.css('a.newsFeed_item_link::attr(href)').getall()
        newsSummaryUrls = [link for link in htmllinks if 'pickup' in link]
        print(f'parse_titlelist_test listcount {len(newsSummaryUrls)}')
        for newsSummaryUrl in newsSummaryUrls:
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
                date=articleHtml.time.get_text(),
                title=articleHtml.title.get_text(),
                body=articleBodyTag.get_text()
                )