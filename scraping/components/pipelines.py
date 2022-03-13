import sys
print(sys.path)
from djangodir.articles.connections import DBOperation
from scraping.morph_analysis import extract_noun

class ArticlePipeline:

    db_operation = DBOperation()
    
    def process_item(self, item, spider):
        item['title'] = item['title'].replace(' - Yahoo!ニュース', '').replace('\u3000', '')
        item['body'] = item['body'].replace('\u3000', '').replace('\n', '')
        item['noun'] = extract_noun(item['body'])
        self.db_operation.save_item(item)
        return item
