from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from djangodir.project import settings

class Article(models.Model):
    """ニュース記事を保存するモデル。一つの記事を一つのArticleに格納する。

    id       Articleの識別子

    url      記事の参照元URL

    category 参照元での記事の分類

    date     記事に書かれている日付

    title    記事の見出し

    body     記事本文

    noun     記事本文から抽出した名詞リスト
    """
    class meta:
        app_label='articles'
    
    id = models.AutoField(primary_key=True)
    url = models.URLField(unique=True)
    category = models.CharField(max_length=20, default='domestic')
    date = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    body = models.TextField()
    noun = models.TextField()

    def __str__(self):
        return self.title

    def get_id(self):
        return str(self.id)
            
class Preference(models.Model):
    """Userと一対一で紐付けられた、記事に対するUserの嗜好を保存するモデル。
    
    user                     このPreferenceに紐付けられたUserモデル

    good_ids                 Userが'いいね'と評価した記事のID

    good_nouns               Userが'いいね'と評価した記事から抽出した名詞群。
                             'いいね'評価がゼロの場合、または評価が反映されて
                             いない場合は空のstrが格納される

    recommended_id_rate_pair Userが'いいね'と評価した記事内の名詞群'good_nouns'
                             に対する他の記事の名詞群の一致率を求めて、
                             記事IDと一致率のペアにしたもの。
                             'いいね'評価がゼロの場合、または評価が反映されて
                             いない場合は空のstrが格納される

    uninterested_ids         Userが'興味なし'と評価した記事のID

    uninterested_nouns       Userが'興味なし'と評価した記事から抽出した名詞群。
                             '興味なし'評価がゼロの場合、または評価が反映されて
                             いない場合は空のstrが格納される

    rejected_id_rate_pair    Userが'興味なし'と評価した記事内の名詞群
                             'uninterested_nouns'に対する他の記事の名詞群の
                             一致率を求めて、記事IDと一致率のペアにしたもの。
                             '興味なし'評価がゼロの場合、または評価が反映されて
                             いない場合は空のstrが格納される
    """

    class meta:
        app_lavel = 'articles'
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    good_ids = models.TextField(default='')
    good_nouns = models.TextField(default='')
    recommended_id_rate_pair = models.TextField(default='')
    uninterested_ids = models.TextField(default='')
    uninterested_nouns = models.TextField(default='')
    rejected_id_rate_pair = models.TextField(default='')

    def get_good_list(self):
        """good評価された記事のIDが文字列で保存されているのをリストに変換する"""
        return [] if self.good_ids == '' else self.good_ids.split(',')

    def get_uninterested_list(self):
        """uninterested評価された記事のIDが文字列で保存されているのをリストに変換する"""
        return [] if self.uninterested_ids == '' else self.uninterested_ids.split(',')

    def evaluate_good(self, article_id):
        """goodと評価された記事のIDをgood評価リストに追加するメソッド
        既にリストにある場合にはリストから削除する。
        uninterested評価リストからも同IDが削除される
        """
        #文字列で保存されているのをリストに変換する
        good_id_list = self.get_good_list()
        #既にgood評価リストに含まれていれば除去する
        if article_id in good_id_list:
            good_id_list.remove(article_id)
        else:
            #good評価リストになければ追加
            good_id_list.append(article_id)
            #uninterested評価リストにこの記事IDがあった場合には除去する
            uninterested_id_list = self.get_uninterested_list()
            if article_id in uninterested_id_list:
                uninterested_id_list.remove(article_id)
                self.uninterested_ids = ','.join(uninterested_id_list)
        self.good_ids = ','.join(good_id_list)
        self.save()

    def evaluate_uninterest(self, article_id):
        """uninterestedと評価された記事のIDをuninterested評価リストに追加するメソッド
        既にリストにある場合にはリストから削除する。
        good評価リストからも同IDが削除される
        """
        #文字列で保存されているのをリストに変換する
        uninterested_id_list = self.get_uninterested_list()
        #既にuninterested評価リストに含まれていれば除去する
        if article_id in uninterested_id_list:
            uninterested_id_list.remove(article_id)
        else:
            #uninterested評価リストになければ追加
            uninterested_id_list.append(article_id)
            #good評価リストにこの記事IDがあった場合には除去する
            good_id_list = self.get_good_list()
            if article_id in good_id_list:
                good_id_list.remove(article_id)
                self.good_ids = ','.join(good_id_list)
        self.uninterested_ids = ','.join(uninterested_id_list)
        self.save()

    def category_clear(self, category):
        """引数で受け取ったカテゴリーの記事の評価を全て消去する"""
        good_id_list = self.get_good_list()
        uninterested_id_list = self.get_uninterested_list()
        category_articles = Article.objects.filter(category=category)
        for article in category_articles:
            article_id = str(article.id)
            if article_id in good_id_list:
                good_id_list.remove(article_id)
            if article_id in uninterested_id_list:
                uninterested_id_list.remove(article_id)
        self.good_ids = ','.join(good_id_list)
        self.uninterested_ids = ','.join(uninterested_id_list)
        
        self.save()

    def all_clear(self):
        """全ての評価とその評価にもとづいた結果を消去する"""
        self.good_ids = ''
        self.uninterested_ids = ''
        self.good_nouns = ''
        self.uninterested_nouns = ''
        self.recommended_id_rate_pair = ''
        self.rejected_id_rate_pair = ''
        self.save()

    def get_recommended_id_rate_dict(self):
        """strで保存されているrecommended_id_rate_pairをdictで返す"""
        return self.convert_str_to_dict(self.recommended_id_rate_pair)

    def set_recommended_id_rate_dict(self, id_rate_dict):
        """dictで渡されたrecommended_id_rate_pairをstrで保存する"""
        self.recommended_id_rate_pair = self.convert_dict_to_str(id_rate_dict)

    def get_rejected_id_rate_dict(self):
        """「興味なし」の評価から算出したdict{記事ID:一致率}を取得する"""
        return self.convert_str_to_dict(self.rejected_id_rate_pair)

    def set_rejected_id_rate_dict(self, id_rate_dict):
        """「興味なし」の評価から算出したdict{記事ID:一致率}をデータベースに保存する"""
        self.rejected_id_rate_pair = self.convert_dict_to_str(id_rate_dict)

    def convert_dict_to_str(self, id_rate_dict):
        """引数として受け取ったdictの':'や','を文字列に変換してstrで返す関数"""
        id_rate_pair_list = [str(key + ':' + val) for key, val in id_rate_dict.items()]
        return ','.join(id_rate_pair_list)

    def convert_str_to_dict(self, saved_str):
        """引数として受け取ったstrをdictに変換して返す関数"""
        pair_str_list = [] if saved_str == '' else saved_str.split(',')
        pair_list_list = [pair.split(':') for pair in pair_str_list]
        return {id_rate_pair[0]:id_rate_pair[1] for id_rate_pair in pair_list_list}

class MyUserManager(BaseUserManager):
    """カスタムユーザー使用のために作成"""
    use_in_migrations = True
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """公式の推奨に従い、User関連の変更に対応するために
    作成したカスタムユーザーモデル。現時点で特段変更点は無い。
    """
    class Meta:
        verbose_name = ("user")

    username = models.CharField(max_length=30, unique=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.get_username()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
