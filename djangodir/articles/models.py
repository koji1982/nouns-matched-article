from django.db import models
import structlog

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

    def __str__(self):
        return self.title

    def clear_evaluation(self):
        self.evaluation = Article.NOT_EVALUATED
        self.save()

    def evaluate(self, eval_value):
        self.evaluation = Article.NOT_EVALUATED if (self.evaluation == eval_value) else eval_value
        self.save()