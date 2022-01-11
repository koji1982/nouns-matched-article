from django.db import models

class Article(models.Model):
    class meta:
        app_label='articles'
    
    url = models.URLField()
    date = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    body = models.TextField()
    noun = models.TextField()
