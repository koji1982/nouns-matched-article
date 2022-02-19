from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
import structlog

def article_response(request):
    return render(request, 'app/frame.html')

def left_frame(request):
    logger = structlog.get_logger(__name__)
    logger.info(request.method)
    content = {}
    if request.method == "POST":
        logger.info("from POST")
        if "reflect" in request.POST:
            content['records'] = 'src_link&it'
            logger.info("from reflect")
        elif "reset" in request.POST:
            content['records'] = Article.objects.all().filter(category='local')
            logger.info("from reset")
    return render(request, 'app/pages.html')

def right_frame(request):
    context = {
        'records':Article.objects.all()
    }
    return render(request, 'app/src_link.html', context)

def init_link(request):
    # test_article = Article.objects.all().filter(url='https:/news.yahoo.co.jp/articles/3635ae421328e9350c6776eca7f45c1aa1f3d23a')
    # logger = structlog.get_logger(__name__)
    # if test_article is None:
    #     logger.info('url get empty !!!')
    # else:
    #     logger.info(str(test_article))
    articles = Article.objects.all().filter(category='domestic')
    context = {
        'records': articles,
        'category':'国内'
    }
    logger = structlog.get_logger(__name__)
    logger.info(Article.objects.count())
    logger.info('right_frame loaded')
    return render(request, 'app/src_link.html', context)

def article_link(request, clicked_category):
    # test_article = Article.objects.all().filter(url='https:/news.yahoo.co.jp/articles/3635ae421328e9350c6776eca7f45c1aa1f3d23a')
    # logger = structlog.get_logger(__name__)
    # if test_article is None:
    #     logger.info('url get empty !!!!!')
    # else:
    #     logger.info(str(test_article))
    articles = Article.objects.all().filter(category=clicked_category)
    context = {
        'records': articles,
        'category':get_category_jp(clicked_category),
    }
    # logger = structlog.get_logger(__name__)
    # logger.error("from article_link")
    # checked_list = []
    # radio_length = len(context['records'])
    # logger.error(request.POST.get('btnradio'))
    # logger.error(request.POST.get('1'))
    # logger.error(request.POST.get('2'))
    # logger.error(request.POST.getlist('btnradio'))
    # logger.error(request.POST.getlist('3'))
    # for element in checked_array:
    #     logger.error(str(element))
    # for index in range(radio_length):
    #     logger.error(request.GET.get(str(index)))
    #     if value is not None:
    #         checked_list.append(value)
    # logger.error(checked_list)
    logger = structlog.get_logger(__name__)
    logger.info(Article.objects.count())
    logger.info('right_frame loaded')
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


def get_category_jp(category):
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
    return category_dict[category]

def get_category_en(category):
    category_dict = {
        '国内': 'domestic',
        '国際': 'world',
        '経済': 'business',
        'エンタメ': 'entertainment',
        'スポーツ': 'sports',
        'IT': 'it',
        '科学': 'science',
        '地域': 'local'
    }
    return category_dict[category]