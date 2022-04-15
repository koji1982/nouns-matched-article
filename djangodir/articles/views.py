import os
import environ
from urllib.parse import urlencode
from pathlib import Path
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from articles.models import *
from articles.selection import apply_choices
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
        #入力が有効な場合は保存して完了画面へリダイレクト
        form.save()
        #完了画面へ送るデータをurlにまとめる
        completed_url = reverse('articles:signup_completed')
        param_dict = {'username': username, 'password': '*' * len(password1)}
        param_in_url = urlencode(param_dict)
        url_with_parameters = f'{completed_url}?{param_in_url}'
        return redirect(url_with_parameters)
    else:
        error_message += '\n入力内容が無効とみなされました'
        context['error'] = error_message
        return render(request, 'app/signup.html', context)

def signup_completed(request):
    content = {
        'username': request.GET.get('username'),
        'password': request.GET.get('password')
    }
    return render(request, 'app/signup_completed.html', content)

def login_process(request):

    if request.method == 'GET':
        return render(request, 'app/login.html', {'form': LoginForm()})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        #Preferenceが作られていない場合は作成する
        if not Preference.objects.filter(username=user).exists():
            Preference.objects.create(username=user)
        return redirect('/')
    else:
        error_message = '認証に失敗しました'
        return render(request, 'app/login.html', {'form': LoginForm(), 'error': error_message})

def login_guest_user(request):
    #パスワードを環境変数から取得
    env = environ.Env()
    env.read_env(os.path.join(Path(__file__).resolve().parent.parent.parent, '.django_env'))
    #guest_userが存在するかをチェック
    if not User.objects.filter(username=GUEST_USERNAME).exists():
        #なければguest_userを作成する
        data = {'username': GUEST_USERNAME, 'password1': env('GUEST_PASSWORD'), 'password2': env('GUEST_PASSWORD')}
        form = SignupForm(data=data)
        form.save()
    #guest_userとして認証
    user = authenticate(username=GUEST_USERNAME, password=env('GUEST_PASSWORD'))
    #guest_userとしてログイン
    login(request, user)
    #Preferenceが作られていない場合は作成する
    if not Preference.objects.filter(username=user).exists():
        Preference.objects.create(username=user)
    #記事選択のページへ転送
    return redirect('/')

def logout_reopen(request):
    #djangoユーザーのログアウト
    logout(request)
    #先頭のページへ転送
    return redirect('/login')

def left_frame(request):
    content = {
        'user': str(request.user)
    }
    return render(request, 'app/pages.html', content)

def article_link(request, clicked_category='domestic'):
    articles = Article.objects.filter(category=clicked_category)
    context = {
        'records': articles,
        'category':get_category_jp(clicked_category),
        'preference': Preference.objects.get(username=request.user)
    }
    return render(request, 'app/src_link.html', context)

def all_clear(request):
    preference = Preference.objects.get(username=request.user)
    preference.all_clear()
    return redirect('/src_link')

def category_clear(request, category_in_jp):
    category_in_en = get_category_en(category_in_jp)
    preference = Preference.objects.get(username=request.user)
    preference.category_clear(category_in_en)
    context = {
        'records': Article.objects.filter(category=category_in_en),
        'category': category_in_jp,
        'preference': preference
    }
    return render(request, 'app/src_link.html', context)

def eval_good(request, clicked_category, article_title):
    evaluated_article = Article.objects.get(title=article_title)
    current_user_pref = Preference.objects.get(username=request.user)
    current_user_pref.evaluate_good(evaluated_article.get_id())
    context = {
        'records': Article.objects.filter(category=clicked_category),
        'category':get_category_jp(clicked_category),
        'preference': Preference.objects.get(username=request.user)
    }
    
    return render(request, 'app/src_link.html', context)

def eval_uninterested(request, clicked_category, article_title):
    evaluated_article = Article.objects.get(title=article_title)
    current_user_pref = Preference.objects.get(username=request.user)
    current_user_pref.evaluate_uninterest(evaluated_article.get_id())
    context = {
        'records': Article.objects.filter(category=clicked_category),
        'category':get_category_jp(clicked_category),
        'preference': Preference.objects.get(username=request.user)
    }
    return render(request, 'app/src_link.html', context)

def loading(request):
    '''ローディング画面を呼び出して描画する'''
    return render(request, 'app/loading.html')

def call_apply_choices(request):
    apply_choices(request.user)
    return redirect('/result_positive')

def result_positive(request):
    id_rate_dict = Preference.objects.get(username=request.user).get_recommended_id_rate_dict()
    rate_articles = []
    for id, rate in id_rate_dict.items():
        article = Article.objects.get(id=id)
        rate_articles.append((rate, article))
    sorted_rate_articles = sorted(rate_articles, key=lambda pair: pair[0], reverse=True)
    context = {
        'result_title': '「いいね」評価の記事から抽出された語群（名詞）と\nその語群に対する各記事の一致率',
        'recommendations': sorted_rate_articles,
        'eval_nouns': Preference.objects.get(username=request.user).good_nouns,
    }
    return render(request, 'app/result.html', context)

def result_negative(request):
    id_rate_dict = Preference.objects.get(username=request.user).get_rejected_id_rate_dict()
    rate_articles = []
    for id, rate in id_rate_dict.items():
        article = Article.objects.get(id=id)
        rate_articles.append((rate, article))
    sorted_rate_articles = sorted(rate_articles, key=lambda pair: pair[0], reverse=True)
    context = {
        'result_title': '「興味なし」評価の記事から抽出された語群（名詞）と\nその語群に対する各記事の一致率',
        'recommendations': sorted_rate_articles,
        'eval_nouns': Preference.objects.get(username=request.user).uninterested_nouns,
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