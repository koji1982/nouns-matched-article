from django.shortcuts import render
from django.http import HttpResponse
from .forms import PracticeForm
from .models import Article

def article_response(request):
    return render(request, 'app/frame.html')

def left_frame(request):
    content = {
        'select':'選択',
        'reflect':'反映',
        'result':'結果',
        'acumulate':'累積',
        'figure':'図表',
        'reset':'リセット'
    }
    return render(request, 'app/pages.html', content)

def right_frame(request):
    context = {
        'records':Article.objects.all(),
        'domestic':'国内',
        'international':'国際',
        'economy':'経済',
        'entertaiment':'エンタメ',
        'sport':'スポーツ',
        'it':'IT',
        'science':'科学',
        'local':'地域'
    }
    return render(request, 'app/src_link.html', context)

def init_link(request):
    context = {
        'records':Article.objects.all().filter(category='domestic')
    }
    return render(request, 'app/src_link.html', context)

def article_link(request, clicked):
    context = {
        'records':Article.objects.all().filter(category=clicked)
    }
    return render(request, 'app/src_link.html', context)
# def index(request):
#     insert_dict = {
#         'insert_from_view_dict':"views.pyから渡されるdict",
#         '2nd_key':"2nd value",
#         'list_key':['index_1', 'index_2', 'index_3'],
#         'form':PracticeForm(),
#         'insert_forms':'入力されていません'
#     }
#     if(request.method == 'POST'):
#         insert_dict['insert_forms'] = '文字列:' + request.POST['text'] + '\n整数型:' + request.POST['num']
#         insert_dict['form'] = PracticeForm(request.POST)
#     return render(request, 'app/index.html', insert_dict)
    
# def info(request):
#     articles = Article.objects.all()
#     article_values = Article.objects.values()
#     display_dict = {
#         'title':'test',
#         'list_1':'articles',
#         'list_2':'article_values'
#     }
#     return render(request, 'app/index.html', display_dict)