from django.db import models


class Article(models.Model):
    
    NOT_EVALUATED = 0
    EVAL_GOOD = 1
    EVAL_UNINTERESTED = 2

    class meta:
        app_label='articles'
    
    url = models.URLField(unique=True)
    category = models.CharField(max_length=15, default='domestic')
    date = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    body = models.TextField()
    noun = models.TextField()
    evaluation = models.IntegerField(default=0)
    rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    def evaluate(self, eval_value):
        '''
        evaluationフィールドの変更を行う関数。
        評価値として有効な1または2のみが引数として渡される
        ことを前提としている
        '''
        if (eval_value != Article.EVAL_GOOD) and (eval_value != Article.EVAL_UNINTERESTED):
            raise ValueError
        self.evaluation = Article.NOT_EVALUATED if (self.evaluation == eval_value) else eval_value
        self.save()

    def clear_evaluation(self):
        self.evaluation = Article.NOT_EVALUATED
        self.save()
