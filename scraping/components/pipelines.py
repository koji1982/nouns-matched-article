from djangodir.articles.connections import DBOperation
from database import ArticleDB
from scraping.analysis import extract_noun

class ScrapeArticlePipeline:

    db_operation = DBOperation()
    
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item['title'] = item['title'].replace(' - Yahoo!ニュース', '').replace('\u3000', '')
        item['body'] = item['body'].replace('\u3000', '').replace('\n', '')
        item['noun'] = extract_noun(item['body'])
        self.db_operation.save_item(item)
        return item

    def close_spider(self, spider):
        pass