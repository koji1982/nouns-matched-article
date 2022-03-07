from django.test import TestCase
from scraping.components.pipelines import ArticlePipeline
from scraping.components.items import ArticleItem
from scraping.components.spiders.spider import ArticleSpider
from articles.models import Article

class ArticlePipelineTest(TestCase):
    
    def test_process_item_save_item_as_article(self):
        """process_item()がitemをArticleとして保存することを確認する"""
        self.assertEqual(Article.objects.count(), 0)

        test_url = 'https://dummy_url_100'
        article_item = get_test_item(test_url)
        article_pipeline = ArticlePipeline()
        article_pipeline.process_item(article_item, ArticleSpider())

        self.assertEqual(Article.objects.count(), 1)
        saved_article = Article.objects.get(url=test_url)
        self.assertEqual(saved_article.url, test_url)

    def test_process_item_add_noun_field(self):
        """process_item()がitemには含まれていない'noun'フィールドを
        追加していることを確認
        """
        test_url = 'https://dummy_url_100'
        article_item = get_test_item(test_url)
        with self.assertRaises(KeyError):
            article_item['noun']
        article_pipeline = ArticlePipeline()
        article_pipeline.process_item(article_item, ArticleSpider())
        
        saved_article = Article.objects.get(url=test_url)
        self.assertTrue('dummy'in saved_article.noun)

    def test_process_item_replace_specific_characters(self):
        """process_item()が改行コードなど一部の文字列を
        置き換えていることを確認
        """
        test_url = 'https://dummy_url_100'
        article_item = ArticleItem(url=test_url,
                                   category='domestic',
                                   date='1/1(土) 22:07',
                                   title='dummy_title_100\u3000 - Yahoo!ニュース\u3000',
                                   body='dummy_\u3000body_\u3000100')
        article_pipeline = ArticlePipeline()
        article_pipeline.process_item(article_item, ArticleSpider())

        saved_article = Article.objects.get(url=test_url)
        self.assertFalse(' - Yahoo!ニュース' in saved_article.title)
        self.assertFalse('\u3000' in saved_article.body)

    def test_process_item_with_none_item_arg(self):
        """process_item()に対して、ArticleItemではなくNoneが渡された場合に
        Errorを送出する
        """
        article_pipeline = ArticlePipeline()
        #ArticleItemではなくNoneが渡された場合
        with self.assertRaises(TypeError):
            article_pipeline.process_item(None, ArticleSpider())
    
    def test_process_item_with_spider_arg_none_complete_process(self):
        """process_item()内ではパラメータのspiderを使用していないので(シグネチャとしては必要)
        spiderの代わりにNoneが渡された場合でも問題なく動作する
        """
        self.assertEqual(Article.objects.count(), 0)

        article_item = get_test_item()
        article_pipeline = ArticlePipeline()
        article_pipeline.process_item(article_item, None)

        print(Article.objects.all()[0].title)

        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.all()[0].title, 'dummy_title_100')
    
    def test_process_item_with_wrong_argument_raises_error(self):
        """process_item()に対して、ArticleItemではなくNoneが渡されたり
        フィールドが入力されていないArticleItemが渡された時にErrorを送出する
        """
        article_pipeline = ArticlePipeline()
        #body無しのArticleItemが渡された場合
        item_without_body = ArticleItem(url='https://dummy_url_101',
                                        category='domestic',
                                        date='1/1(土) 22:07',
                                        title='dummy_title_101')
        with self.assertRaises(KeyError):
            article_pipeline.process_item(item_without_body, ArticleSpider())
        #title無しのArticleItemが渡された場合
        item_without_title = ArticleItem(url='https://dummy_url_102',
                                         category='domestic',
                                         date='1/1(土) 22:07',
                                         body='dummy_body_102')
        with self.assertRaises(KeyError):
            article_pipeline.process_item(item_without_title, ArticleSpider())

    def test_process_item_lack_arg_raises_error(self):
        """process_item()に渡す引数が足りない場合はエラーが送出される"""
        article_item = get_test_item()
        article_pipeline = ArticlePipeline()
        #Spiderが渡されなかった場合
        with self.assertRaises(TypeError):
            article_pipeline.process_item(item=article_item)
        #Itemが渡されなかった場合
        with self.assertRaises(TypeError):
            article_pipeline.process_item(spider=ArticleSpider())

def get_test_item(url='https://dummy_url_100'):
    return ArticleItem(url=url,
                       category='domestic',
                       date='1/1(土) 22:07',
                       title='dummy_title_100',
                       body='dummy_body_100')