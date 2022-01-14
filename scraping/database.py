import MySQLdb
import os
import traceback

class ArticleDB:

    _db = None

    @staticmethod
    def create_news():
        cursor = ArticleDB._db.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS news CHARACTER SET utf8mb4;')
        cursor.execute('USE news;')
        cursor.execute('CREATE TABLE IF NOT EXISTS articles (url VARCHAR(768) UNIQUE,'
                       'date TEXT, title TEXT, body TEXT, noun TEXT) CHARACTER SET utf8mb4;')
        ArticleDB._db.commit()
        cursor.close()

    # @staticmethod
    # def create_selected():
    #     cursor = ArticleDB._db.cursor()
    #     cursor.execute('CREATE DATABASE IF NOT EXISTS selected CHARACTER SET utf8mb4;')
    #     cursor.execute('USE selected;')
    #     cursor.execute('CREATE TABLE IF NOT EXISTS recommend_rates (url VARCHAR(768) UNIQUE,'
    #                    'nouns TEXT, rate_list TEXT, is_valid BOOLEAN;')

    @staticmethod
    def connect(dbname):
        # env = environ.Env()
        # env.read_env(os.path.join(os.path.dirname(__file__), 'sql_config'))
        ArticleDB._db = MySQLdb.connect(host=os.environ['MYSQL_HOST'], user=os.environ['MYSQL_ROOT_USER'],
                                        passwd=os.environ['MYSQL_PASSWORD'],
                                        use_unicode=True)
        # dbname = env('db')
        print(os.environ['MYSQL_ROOT_PASSWORD'])
        cursor = ArticleDB._db.cursor()
        cursor.execute('SHOW DATABASES;')
        databases = cursor.fetchall()
        for i, database in enumerate(databases):
            if dbname in database:
                break
            if (len(databases)-1) <= i:
                ArticleDB.create_news()
        cursor.execute('USE news')
        cursor.close()

    @staticmethod
    def close():
        if ArticleDB._db is not None:
            ArticleDB._db.close()
        ArticleDB._db = None

    @staticmethod
    def insert(item):
        if ArticleDB._db is None:
            ArticleDB.connect('news')
        try:
            sql = ( 'INSERT INTO articles (url, date, title, body, noun) '
                    'VALUES (%s, %s, %s, %s, %s);')
            cursor = ArticleDB._db.cursor()
            cursor.execute(sql, (item['url'], item['date'], item['title'],
                                 item['body'], item['noun']))
        except:
            traceback.print_exc()
        ArticleDB._db.commit()
        cursor.close()

    @staticmethod
    def getAllBody():
        if ArticleDB._db is None:
            ArticleDB.connect('news')
        cursor = ArticleDB._db.cursor()
        sql = "SELECT url, body FROM articles;"
        cursor.execute(sql)
        repr(cursor.fetchall())
        cursor.close()

    @staticmethod
    def getBody(target):
        if ArticleDB._db is None:
            ArticleDB.connect('news')
        with ArticleDB._db.cursor() as cursor:
            sql = "SELECT url, body FROM articles WHERE url='%s';"
            cursor.execute(sql % target)
            return cursor.fetchone()

    @staticmethod
    def getAllNoun():
        if ArticleDB._db is None:
            ArticleDB.connect('news')
        with ArticleDB._db.cursor() as cursor:
            sql = "SELECT url, noun FROM articles;"
            cursor.execute(sql)
            return cursor.fetchall()
