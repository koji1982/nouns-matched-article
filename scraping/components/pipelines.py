from djangodir.articles.connections import DBOperation

class ArticlePipeline:

    db_operation = DBOperation()
    
    def process_item(self, item, spider):
        """scrapyのclawler実行時、spider.parse後に呼ばれるメソッド
        ここでは文字情報の整理とDjangoデータベースへの保存を行っている
        """
        item['title'] = item['title'].replace(' - Yahoo!ニュース', '').replace('\u3000', '').replace('/', '')
        item['body'] = item['body'].replace('\u3000', '').replace('\n', '')
        self.db_operation.register_item(item)
        return item
