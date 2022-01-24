from django.shortcuts import render
from django.http import HttpResponse
from .forms import PracticeForm
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
    context = {
        'records':Article.objects.all().filter(category='domestic'),
        'category':'国内'
    }
    return render(request, 'app/src_link.html', context)

def article_link(request, clicked_category):
    context = {
        'records':Article.objects.all().filter(category=clicked_category),
        'category':get_category_name(clicked_category)
    }
    return render(request, 'app/src_link.html', context)

def get_category_name(category):
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