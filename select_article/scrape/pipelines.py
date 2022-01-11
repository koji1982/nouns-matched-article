from djangodir.articles.django_db import DBConnector
from database import ArticleDB
from word_analyze import extract_noun

class ScrapeArticlePipeline:
    db_connector = DBConnector()
    def open_spider(self, spider):
        # ArticleDB.connect('news')
        self.db_connector.init_django_db()
        pass

    def process_item(self, item, spider):
        item['title'] = item['title'].replace(' - Yahoo!ニュース', '').replace('\u3000', '')
        item['body'] = item['body'].replace('\u3000', '').replace('\n', '')
        item['noun'] = extract_noun(item['body'])
        # ArticleDB.insert(item)
        self.db_connector.save_article(item)
        print('     --           from pipeline          -- ')
        return item

    def close_spider(self, spider):
        # ArticleDB.close()
        pass