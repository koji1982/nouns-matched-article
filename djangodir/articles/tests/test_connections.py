from django.test import TestCase
from articles.models import Article
from articles.connections import DBOperation
from scraping.components.items import ArticleItem

class ConnectionsTest(TestCase):

    def test_register_item(self):
        """register_item()が引数として受け取ったitemを
        保存することを確認する
        """
        #ArticleItemを作成し、Articleとしてデータベースに登録されていないことを確認
        test_item = ArticleItem(url='test_url',
                                category='test_category',
                                date='test_date',
                                title='test_title',
                                body='test_body' )
        self.assertFalse(Article.objects.filter(url=test_item['url']).exists())

        #テスト対象
        db_operation = DBOperation()
        db_operation.register_item(test_item)
        
        #Articleとしてデータベースに登録されていることを確認
        self.assertTrue(Article.objects.filter(url=test_item['url']).exists())

    def test_register_item_ignore_duplicate_item(self):
        """register_item()が既に保存されている記事と重複する
        itemを渡された時にそのまま終了することを確認する
        """
        test_item = ArticleItem(url='test_url',
                                category='test_category',
                                date='test_date',
                                title='test_title',
                                body='test_body' )
        duplicate_item = ArticleItem(url='test_url',
                                     category='test_category',
                                     date='test_date',
                                     title='test_title',
                                     body='test_body' )
        #同じ内容のitemの片方を先に一つ保存する
        self.assertFalse(Article.objects.filter(url=test_item['url']).exists())
        db_operation = DBOperation()
        db_operation.register_item(test_item)
        self.assertTrue(Article.objects.filter(url=test_item['url']).exists())
        self.assertEqual(Article.objects.count(), 1)

        #テスト対象
        db_operation.register_item(duplicate_item)
        #変わっていないことを確認
        self.assertTrue(Article.objects.filter(url=test_item['url']).exists())
        self.assertEqual(Article.objects.count(), 1)