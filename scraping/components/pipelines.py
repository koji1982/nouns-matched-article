from djangodir.articles.external import DBConnection
from database import ArticleDB
from scraping.analysis import extract_noun

class ScrapeArticlePipeline:
    db_connection = DBConnection()
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item['title'] = item['title'].replace(' - Yahoo!ニュース', '').replace('\u3000', '')
        item['body'] = item['body'].replace('\u3000', '').replace('\n', '')
        item['noun'] = extract_noun(item['body'])
        # ArticleDB.insert(item)
        self.db_connection.save_article(item)
        print('     --           from pipeline          -- ')
        return item

    def close_spider(self, spider):
        # ArticleDB.close()
        pass