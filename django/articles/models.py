from django.db import models

class Article(models.Model):
    url = models.URLField()
    date = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    body = models.TextField()
    noun = models.TextField()
