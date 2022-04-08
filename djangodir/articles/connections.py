# Djangoの外から呼ばれることを前提としてるため、
# ファイルを読み込む前にDjangoの設定を用意する
import django
import os
import sys
from pprint import pprint
from pathlib import Path
from django.db import IntegrityError
django_root = str(Path(__file__).resolve().parent.parent)
sys.path.append(django_root)
pprint(django_root)
pprint(sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from articles.models import Article
from articles.nlp import extract_noun


class DBOperation:

    def register_item(self, item):
        """scrapyフレームワークのitemを受け取りDjango内の
        データベースに保存するメソッド
        """
        #同じ記事が既にある場合はそのまま終了する
        if Article.objects.filter(title=item['title']).exists():
            return
        #一致率の計算に使う名詞を先に抽出しておく
        item['noun'] = extract_noun(item['body'])
        #Articleの保存
        Article.objects.create(url=item['url'], category=item['category'],
                               date=item['date'], title=item['title'],
                               body=item['body'], noun=item['noun'])
