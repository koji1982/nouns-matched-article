import structlog
from django.db import models
from django.db.models import Q
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth import authenticate, login
from djangodir.project import settings
from scraping.morph_analysis import *

class Article(models.Model):

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
            
class Preference(models.Model):

    class meta:
        app_lavel = 'articles'

    username = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    good_ids = models.TextField()
    good_nouns = models.TextField()
    recommended_id_rate_pair = models.TextField()
    uninterested_ids = models.TextField()
    uninterested_nouns = models.TextField()
    rejected_id_rate_pair = models.TextField()

    def is_evaluated_good(self, article_id):
        good_id_list = self.good_ids.split(',')
        return (article_id in good_id_list)

    def is_evaluated_uninterested(self, article_id):
        uninterested_id_list = self.uninterested_ids.split(',')
        return (article_id in uninterested_id_list)

    def evaluate_good(self, article_id):
        good_id_list = self.good_ids.split(',')
        if article_id in good_id_list:
            good_id_list.remove(article_id)
        else:
            good_id_list.append(article_id)
        self.save()

    def evaluate_uninterest(self, article_id):
        uninterested_id_list = self.uninterested_ids.split(',')
        if article_id in uninterested_id_list:
            uninterested_id_list.remove(article_id)
        else:
            uninterested_id_list.append(article_id)
        self.save()

    def clear_evaluation(self):
        # self.evaluation = Preference.NOT_EVALUATED
        # self.save()
        pass

class MyUserManager(BaseUserManager):

    use_in_migrations = True
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        # if email is None:
        #     raise ValueError('E-mailが入力されていません')
        
        import structlog
        logger = structlog.get_logger(__name__)
        logger.info('create_user_1')

        username = self.model.normalize_username(username)
        logger.info('create_user_2')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        logger.info('create_user_3')
        return user

    def create_guest_user(self):
        user = self.model(username='guest')
        user.save()

class User(AbstractBaseUser):

    class Meta:
        verbose_name = ("user")

    username = models.CharField(max_length=30, unique=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_username()
