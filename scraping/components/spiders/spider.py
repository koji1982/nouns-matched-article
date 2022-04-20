import requests
import re
import time
from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scraping.components.items import ArticleItem


class ArticleSpider(CrawlSpider):
    """Yahooニュースの記事を収集するスパイダー。"""

    name = 'article_spider'
    allowed_domains = ['www.yahoo.co.jp', 'news.yahoo.co.jp']
    start_urls = [
        'https://news.yahoo.co.jp/topics/domestic?page=1'
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
        """一つの記事に対して一つのItemを作成する。
        記事リストからリンクをたどり、導入ページを通り過ぎて本文のページで
        記事の取得を行う。クローリング時にScrapyフレームワークから呼ばれる。

        @url https://news.yahoo.co.jp/topics/domestic?page=1
        @returns items 1
        @returns requests 0
        @scrapes url category date title body
        """
        #ニュースカテゴリーごとに呼ばれる関数なのでここでカテゴリーを格納しておく
        url = response.url
        current_category = None
        url_tail = url.split("/")[-1]
        for category in self.categories:
            if re.match(category, url_tail) is not None:
                current_category = category
                break
        #記事リストからリンクを取り出し、各リンクを辿る
        htmllinks = response.css('a.newsFeed_item_link::attr(href)').getall()
        newsSummaryUrls = [link for link in htmllinks if 'pickup' in link]
        for newsSummaryUrl in newsSummaryUrls:
            #導入ページを経由して記事本文へのリンクを取り出す
            newsSummaryResponse = requests.get(newsSummaryUrl)
            newsSummaryHtml = BeautifulSoup(newsSummaryResponse.text, 'html.parser')
            articleLinkTag = newsSummaryHtml.find('a', text=['記事全文を読む', '続きを読む'])
            if articleLinkTag is None:
                continue
            articleUrl = articleLinkTag.get('href')
            #記事本文の取得（本文が分かれて記述されている場合の為にfind_all()で取得）
            articleResponse = requests.get(articleUrl)
            parsed_article = BeautifulSoup(articleResponse.text, 'html.parser')
            article_bodies = parsed_article.find_all('p', class_='highLightSearchTarget')
            intro_body = ''
            for body_part in article_bodies:
                intro_body += body_part.text
            if intro_body is '':
                continue
            #複数ページの場合は、最初のページの本文を渡して関数内で
            #結合したstrを戻り値として受け取る
            body_text = self.get_pagination_text(parsed_article, articleUrl, intro_body)
            yield ArticleItem(url=articleUrl,
                              category=current_category,
                              date=parsed_article.time.get_text(),
                              title=parsed_article.title.get_text(),
                              body=body_text )

    def get_pagination_text(self, parsed_html, src_url, additional_body_text, page_count=1):
        """複数ページの記事の時にリンクを辿って本文を繋げて返すメソッド
        リンクが無い場合は受け取った本文をそのまま返す
        """
        #ページのリンクを取得。無ければそのまま終了する
        pagination_links = parsed_html.find_all('li', class_='pagination_item')
        for pagination_link in pagination_links:
            #次のページへのリンク以外はスキップする
            next_page = '?page=' + str(page_count+1)
            if (pagination_link is None) or (next_page not in str(pagination_link)):
                continue
            #次のページのurlを生成して取得、解析する
            next_url = src_url + next_page
            time.sleep(1.0)
            pagination_response = requests.get(next_url)
            parsed_html = BeautifulSoup(pagination_response.text, 'html.parser')
            #記事本文の取得（本文が分かれて記述されている場合の為にfind_all()で取得）
            extracted_body_text = ''
            next_result_bodies = parsed_html.find_all('p', class_='highLightSearchTarget')
            for body_part in next_result_bodies:
                extracted_body_text += body_part.text
            additional_body_text += extracted_body_text
            #また次のページを探すために再帰呼び出し
            page_count += 1
            additional_body_text = self.get_pagination_text(parsed_html, src_url, additional_body_text, page_count=page_count)
            break
        return additional_body_text