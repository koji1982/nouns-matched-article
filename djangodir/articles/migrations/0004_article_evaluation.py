# Generated by Django 3.2.5 on 2022-02-01 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='evaluation',
            field=models.IntegerField(default=0),
        ),
    ]
