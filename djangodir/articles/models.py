from django.db import models

class Article(models.Model):
    class meta:
        app_label='articles'
    
    url = models.URLField(unique=True)
    category = models.CharField(max_length=15, default='domestic')
    date = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    body = models.TextField()
    noun = models.TextField()

    def __str__(self):
        return self.title