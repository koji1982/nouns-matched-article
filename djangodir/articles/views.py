from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from articles.models import Article
from articles.templatetags.external_functions import *

category_dict = {
        'domestic':'国内',
        'world':'国際',
        'business':'経済',
        'entertainment':'エンタメ',
        'sports':'スポーツ',
        'it':'IT',
        'science':'科学',
        'local':'地域'
    }

def article_response(request):
    return render(request, 'app/frame.html')

def left_frame(request):
    content = {}
    if request.method == "POST":
        if "reflect" in request.POST:
            content['records'] = 'src_link&it'
        elif "reset" in request.POST:
            content['records'] = Article.objects.all().filter(category='local')
    return render(request, 'app/pages.html')

def init_link(request):
    articles = Article.objects.all().filter(category='domestic')
    context = {
        'records': articles,
        'category': '国内'
    }
    return render(request, 'app/src_link.html', context)

def article_link(request, clicked_category):
    articles = Article.objects.all().filter(category=clicked_category)
    context = {
        'records': articles,
        'category':get_category_jp(clicked_category),
    }
    return render(request, 'app/src_link.html', context)

def all_clear(request, category_in_jp):
    category_in_en = get_category_en(category_in_jp)
    for article in Article.objects.all().filter(category=category_in_en):
        article.clear_evaluation()
    context = {
        'records': Article.objects.all().filter(category=category_in_en),
        'category': category_in_jp
    }
    return render(request, 'app/src_link.html', context)

def eval_good(request, clicked_category, article_title):
    evaluated_article = Article.objects.get(title=article_title)
    evaluated_article.evaluate(Article.EVAL_GOOD)
    context = {
        'records': Article.objects.all().filter(category=clicked_category),
        'category':get_category_jp(clicked_category),
    }
    return render(request, 'app/src_link.html', context)

def eval_uninterested(request, clicked_category, article_title):
    evaluated_article = Article.objects.get(title=article_title)
    evaluated_article.evaluate(Article.EVAL_UNINTERESTED)
    context = {
        'records': Article.objects.all().filter(category=clicked_category),
        'category':get_category_jp(clicked_category),
    }
    return render(request, 'app/src_link.html', context)

def loading(request):
    return render(request, 'app/loading.html')

def result(request):
    eval_nouns = apply_choices(request)
    recommendations = []
    if len(eval_nouns) != 0:
        recommendations = Article.objects.order_by('rate').reverse()
    context = {
        'recommendations': recommendations,
        'eval_nouns': eval_nouns
    }
    return render(request, 'app/result.html', context)

def get_category_jp(category):
    return category_dict[category]

def get_category_en(category):
    category_jp_en = {
        '国内': 'domestic',
        '国際': 'world',
        '経済': 'business',
        'エンタメ': 'entertainment',
        'スポーツ': 'sports',
        'IT': 'it',
        '科学': 'science',
        '地域': 'local'
    }
    return category_jp_en[category]