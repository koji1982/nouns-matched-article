import structlog
from django import template
from django.db.models import Q
from scraping.morph_analysis import *
from articles.models import Article

register = template.Library()

@register.filter(name='apply_choices')
def apply_choices(string):
    """利用者が評価した記事に含まれる単語(名詞)をまとめて、
    その単語群と他の記事内の単語がどれだけ一致するかを算出して保存する関数
    """
    #good評価の単語を集める
    good_evals = Article.objects.all().filter(evaluation=Article.EVAL_GOOD)
    #評価がゼロの場合は空のリストを返す
    if good_evals.count() == 0:
        return []
    or_nouns = set()
    for good_article in good_evals:
        good_nouns = set(good_article.noun.split(','))
        or_nouns = or_nouns | good_nouns

    uninterested_evals = Article.objects.all().filter(evaluation=Article.EVAL_UNINTERESTED)
    nouns_list = list(or_nouns)
    good_nouns = ','.join(nouns_list)
    print(good_nouns)
    #未評価の記事を{url:単語}のdictにして一致率を算出する
    src_articles = Article.objects.filter(~Q(evaluation=1), ~Q(evaluation=2))
    url_nouns_dict = {}
    for article in src_articles:
        url_nouns_dict[article.url] = article.noun
    result_url_rate_list = sort_duplicated_nouns_list(good_nouns, url_nouns_dict)
    print(result_url_rate_list)

    update_list = []
    for url_rate in result_url_rate_list:
        article = Article.objects.get(url=url_rate[0])
        article.rate = url_rate[1]
        update_list.append(article)
    Article.objects.bulk_update(update_list, fields=['rate'])

    return good_nouns
    



