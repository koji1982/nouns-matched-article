#
class DBConnector:
    def init_django_db(self):
        # import os
        # import sys
        # from pprint import pprint
        # from pathlib import Path
        # django_root = str(Path(__file__).resolve().parent.parent)
        # sys.path.append(django_root)
        # pprint(django_root)
        # pprint(sys.path)
        # import django
        # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
        # django.setup()
        # from djangodir.articles.models import Article
        pass

    def save_article(self, item):
        import os
        import sys
        from pprint import pprint
        from pathlib import Path
        django_root = str(Path(__file__).resolve().parent.parent)
        project_path = os.path.join(django_root, 'project')
        sys.path.append(django_root)
        sys.path.append(project_path)
        pprint(django_root)
        pprint(sys.path)
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
        django.setup()
        # from django.core.wsgi import get_wsgi_application
        # application = get_wsgi_application()
        from articles.models import Article
        print(item['title'])
        Article.objects.create(url=item['url'], date=item['date'], title=item['title'],
                               body=item['body'], noun=item['noun'])

if __name__ == "__main__":
    DBConnector()
