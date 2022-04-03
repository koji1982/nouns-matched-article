import os
import environ
from pathlib import Path
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from articles.models import *
from articles.templatetags.external_functions import *
from articles.forms import SignupForm, LoginForm

CATEGORY_DICT = {
        'domestic':'国内',
        'world':'国際',
        'business':'経済',
        'entertainment':'エンタメ',
        'sports':'スポーツ',
        'it':'IT',
        'science':'科学',
        'local':'地域'
    }

GUEST_USERNAME = 'ゲスト'

@login_required
def article_response(request):
    return render(request, 'app/frame.html')

def signup(request):
    context = {'form': SignupForm()}
    if request.method == 'GET':
        return render(request, 'app/signup.html', context)
    #ユーザー名、パスワードを入力後、登録ボタンが押された時の処理
    username = request.POST.get('username', '')
    password1 = request.POST.get('password1', '')
    password2 = request.POST.get('password2', '')
    #ユーザー名が既に登録されている場合、未記入の項目がある場合、
    #パスワードの入力を間違えている場合のエラーメッセージを用意する
    error_message = ''
    if User.objects.filter(username=username).exists():
        error_message = 'このユーザー名は既に使用されています'
    if username == GUEST_USERNAME:
        error_message = 'このユーザー名は既に使用されています'
    if (username == '') or (password1 == '') or (password2 == ''):
        error_message = '未記入の項目があります'
    if password1 != password2:
        error_message = '二つのパスワードの入力内容が違っています'
    if error_message != '':
        context['error'] = error_message
        return render(request, 'app/signup.html', context)
    data = {
        'username': username,
        'password1': password1,
        'password2': password2
    }
    form = SignupForm(data=data)
    if form.is_valid():
        form.save()
        return redirect('/login')
    else:
        error_message += '\n入力内容が無効とみなされました'
        context['error'] = error_message
        return render(request, 'app/signup.html', context)

def login_process(request):

    if request.method == 'POST':
        return render(request, 'app/login.html', {'form': LoginForm()})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    else:
        error_message = '認証に失敗しました'
        return render(request, 'app/login.html', {'form': LoginForm(), 'error': error_message})

def login_guest_user(request):
    #パスワードを環境変数から取得
    env = environ.Env()
    env.read_env(os.path.join(Path(__file__).resolve().parent.parent.parent, '.django_env'))
    #guest_userが存在するかをチェック
    User.objects.filter(username=GUEST_USERNAME).delete()
    if not User.objects.filter(username=GUEST_USERNAME).exists():
        #なければguest_userを作成する
        data = {'username': GUEST_USERNAME, 'password1': env('GUEST_PASSWORD'), 'password2': env('GUEST_PASSWORD')}
        form = SignupForm(data=data)
        form.save()
    #guest_userとして認証
    user = authenticate(username=GUEST_USERNAME, password=env('GUEST_PASSWORD'))
    #guest_userとしてログイン
    login(request, user)
    #記事選択のページへ転送
    return redirect('/')

def logout_reopen(request):
    #djangoユーザーのログアウト
    logout(request)
    #先頭のページへ転送
    return redirect('/')

def left_frame(request):
    content = {
        'user': str(request.user)
    }
    if request.method == "POST":
        if "reflect" in request.POST:
            content['records'] = 'src_link&it'
        elif "reset" in request.POST:
            content['records'] = Article.objects.all().filter(category='local')
    return render(request, 'app/pages.html', content)

def init_link(request):
    import structlog
    logger = structlog.get_logger(__name__)
    logger.info(request.user.username)
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
    return CATEGORY_DICT[category]

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