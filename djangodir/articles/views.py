import os
import environ
import operator
from urllib.parse import urlencode
from pathlib import Path
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from articles.models import *
from articles.forms import SignupForm, LoginForm
from articles.nlp import compute_tfidf_cos_similarity
from djangodir.articles.plots import DISPLAY_COUNT, gen_scatter_plot, COLOR_BLUE, COLOR_RED

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
def frame(request):
    """ログイン時に最初に呼ばれることを想定している。
    画面を分けるフレームを定義しているhtmlを返す。
    """
    return render(request, 'app/frame.html')

def signup(request):
    """サインアップ画面として呼ばれる。
    ここでの入力が有効だと判定されると新しいUserが作られる。
    """
    context = {'form': SignupForm()}
    #GETの場合はhtmlを表示して終了
    if request.method == 'GET':
        return render(request, 'app/signup.html', context)
    #以下POSTの場合
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
        #※ローディング画面表示との整合性から、
        # (空欄の場合、ゲストの場合には無効の判定が行われないことから)
        # この時点で無効だと判断された場合はエラーメッセージと共に
        # もう一度サインアップ画面を表示する
        context['error'] = error_message
        return render(request, 'app/signup.html', context)
    data = {
        'username': username,
        'password1': password1,
        'password2': password2
    }
    #Formへ入力データを渡す
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
        #入力が無効な場合はエラーメッセージと共に
        #もう一度サインアップ画面を表示する
        error_message += '\n入力内容が無効とみなされました'
        context['error'] = error_message
        return render(request, 'app/signup.html', context)

def signup_completed(request):
    """サインアップが完了したことを表示する。"""
    content = {
        'username': request.GET.get('username'),
        'password': request.GET.get('password')
    }
    return render(request, 'app/signup_completed.html', content)

def login_process(request):
    """ログイン画面として呼ばれる。
    ログイン成功時にそのUserのPreferenceが存在していない場合は
    新しく作成される。
    """
    #GETの場合はhtmlを表示して終了
    if request.method == 'GET':
        return render(request, 'app/login.html', {'form': LoginForm()})
    #以下POSTの場合
    #入力内容のチェック
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    error_message = ''
    if (username == '') or (password == ''):
        error_message = '未記入の項目があります'
        return render(request,
                      'app/login.html', 
                      {'form': LoginForm(), 'error': error_message})
    data = {
        'username': username,
        'password': password
    }
    #Formに入力データを渡す
    form = LoginForm(data=data)
    if form.is_valid():
        #入力が有効な場合は認証を行い、認証されたUserでログインする
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        #Preferenceが作られていない場合は作成する
        if not Preference.objects.filter(user=user).exists():
            Preference.objects.create(user=user)
        return redirect('/')
    else:
        #入力が無効とされた場合はエラーメッセージと共に
        #もう一度ログイン画面を表示
        error_message = '認証に失敗しました'
        return render(request,
                      'app/login.html',
                      {'form': LoginForm(), 'error': error_message})

def login_guest_user(request):
    """ゲストログインを行う関数。
    ゲストユーザーとそのPreferenceが存在しない場合は
    新しく作成される。
    """
    #パスワードを環境変数から取得
    env = environ.Env()
    env.read_env(os.path.join(Path(__file__).resolve().parent.parent.parent, '.django_env'))
    #guest_userが存在するかをチェック
    if not User.objects.filter(username=GUEST_USERNAME).exists():
        #なければguest_userを作成する
        data = {'username': GUEST_USERNAME,
                'password1': env('GUEST_PASSWORD'),
                'password2': env('GUEST_PASSWORD')}
        form = SignupForm(data=data)
        form.save()
    #guest_userとして認証
    user = authenticate(username=GUEST_USERNAME, password=env('GUEST_PASSWORD'))
    #guest_userとしてログイン
    login(request, user)
    #Preferenceが作られていない場合は作成する
    if not Preference.objects.filter(user=user).exists():
        Preference.objects.create(user=user)
    #記事選択のページへ転送
    return redirect('/')

def logout_reopen(request):
    """ログアウトを行う。完了後はログイン画面にリダイレクトする。"""
    #djangoユーザーのログアウト
    logout(request)
    #先頭のページへ転送
    return redirect('/login')

def left_frame(request):
    """app/frame.htmlで左右に分けたうちの左側を表示する。"""
    content = {
        'user': str(request.user)
    }
    return render(request, 'app/pages.html', content)

def article_link(request, clicked_category='domestic'):
    """カテゴリーごとの記事のリンクを表示する。"""
    articles = Article.objects.filter(category=clicked_category)
    context = {
        'records': articles,
        'category':get_category_jp(clicked_category),
        'preference': Preference.objects.get(user=request.user)
    }
    return render(request, 'app/src_link.html', context)

def all_clear(request):
    """ログイン中のユーザーが行った全ての評価とそこから取得した名詞群、
    一致率を消去する。
    """
    preference = Preference.objects.get(user=request.user)
    preference.all_clear()
    return redirect('/src_link')

def category_clear(request, category_in_jp):
    """選択中のカテゴリーの記事の評価を全て消去する。"""
    category_in_en = get_category_en(category_in_jp)
    preference = Preference.objects.get(user=request.user)
    preference.category_clear(category_in_en)
    context = {
        'records': Article.objects.filter(category=category_in_en),
        'category': category_in_jp,
        'preference': preference
    }
    return render(request, 'app/src_link.html', context)

def eval_good(request, clicked_category, article_title):
    """「いいね」ボタンが押されたときに呼ばれる。
    引数として受け取った記事のIDをPreference.evaluate_good()に渡す。
    """
    evaluated_article = Article.objects.get(title=article_title)
    current_user_pref = Preference.objects.get(user=request.user)
    current_user_pref.evaluate_good(evaluated_article.get_id())
    context = {
        'records': Article.objects.filter(category=clicked_category),
        'category':get_category_jp(clicked_category),
        'preference': Preference.objects.get(user=request.user)
    }
    
    return render(request, 'app/src_link.html', context)

def eval_uninterested(request, clicked_category, article_title):
    """「興味なし」ボタンが押されたときに呼ばれる。
    引数として受け取った記事のIDをPreference.evaluate_uninterested()に渡す。
    """
    evaluated_article = Article.objects.get(title=article_title)
    current_user_pref = Preference.objects.get(user=request.user)
    current_user_pref.evaluate_uninterest(evaluated_article.get_id())
    context = {
        'records': Article.objects.filter(category=clicked_category),
        'category':get_category_jp(clicked_category),
        'preference': Preference.objects.get(user=request.user)
    }
    return render(request, 'app/src_link.html', context)

def loading(request):
    '''ローディング画面を呼び出して描画する'''
    return render(request, 'app/loading.html')

def call_apply_choices(request):
    """compute_tfidf_cos_similarity()を呼び出して、
    結果（推奨記事）の画面にリダイレクトする。
    """
    compute_tfidf_cos_similarity(request.user)
    return redirect('/result_positive')

def result_positive(request):
    """「いいね」評価の記事から取り出した名詞群と、
    そこから算出した一致率を降順で表示する。
    """
    user_preference = Preference.objects.get(user=request.user)
    noun_tfidf_dict = user_preference.get_good_noun_tfidf_dict()
    good_nouns = noun_tfidf_dict.keys()

    id_rate_dict = user_preference.get_recommended_id_rate_dict()
    rate_articles = []
    for id, rate in id_rate_dict.items():
        article = Article.objects.get(id=id)
        rate_articles.append((rate, article))
    sorted_rate_articles = sorted(rate_articles, key=lambda pair: pair[0], reverse=True)
    context = {
        'result_title': '「いいね」評価の記事から抽出された語群（名詞）と\n'\
                        'その語群に対する各記事のTF-IDFベクトルのコサイン類似度',
        'recommendations': sorted_rate_articles,
        'eval_nouns': ','.join(good_nouns),
    }
    return render(request, 'app/result.html', context)

def result_negative(request):
    """「興味なし」評価の記事から取り出した名詞群と、
    そこから算出した一致率を降順で表示する。
    """
    user_preference = Preference.objects.get(user=request.user)
    noun_tfidf_dict = user_preference.get_uninterested_noun_tfidf_dict()
    uninterested_nouns = noun_tfidf_dict.keys()

    id_rate_dict = Preference.objects.get(user=request.user).get_rejected_id_rate_dict()
    rate_articles = []
    for id, rate in id_rate_dict.items():
        article = Article.objects.get(id=id)
        rate_articles.append((rate, article))
    sorted_rate_articles = sorted(rate_articles, key=lambda pair: pair[0], reverse=True)
    context = {
        'result_title': '「興味なし」評価の記事から抽出された語群（名詞）と\n'\
                        'その語群に対する各記事のTF-IDFベクトルのコサイン類似度',
        'recommendations': sorted_rate_articles,
        'eval_nouns': ','.join(uninterested_nouns),
    }
    return render(request, 'app/result.html', context)

def result_graph(request):
    """「いいね」「興味なし」と評価された記事内の単語の影響の大きさを
    図示するページを表示する。
    """
    #Preferenceから保存された計算結果を取得する
    user_preference = Preference.objects.get(user=request.user)
    word_idf_dict = user_preference.get_word_idf_dict()
    good_noun_tfidf_dict = user_preference.get_good_noun_tfidf_dict()
    uninterested_noun_tfidf_dict = user_preference.get_uninterested_noun_tfidf_dict()

    #グラフ生成時に渡すために各語句の、IDF、 TF-IDF、名詞を
    #同じ順番に並べたリストを作成する
    good_ordered_values = make_ordered_values_lists(
                                   good_noun_tfidf_dict, word_idf_dict)
    good_ordered_idf = good_ordered_values[0]
    good_ordered_tfidf = good_ordered_values[1]
    good_ordered_nouns = good_ordered_values[2]
    uninterested_ordered_values = make_ordered_values_lists(
                                   uninterested_noun_tfidf_dict, word_idf_dict)
    uninterested_ordered_idf = uninterested_ordered_values[0]
    uninterested_ordered_tfidf = uninterested_ordered_values[1]
    uninterested_ordered_nouns = uninterested_ordered_values[2]

    #グラフ画像の作成
    good_scatter = gen_scatter_plot(good_ordered_idf,
                                    good_ordered_tfidf,
                                    good_ordered_nouns,
                                    COLOR_BLUE,
                                    '「いいね」と評価された記事内の語句で\n'\
                                    '影響の大きな語（TF-IDF上位30語）の散布図')
    #表示のための'名詞:TF-IDF値'のテキストを作成
    good_noun_count = len(good_noun_tfidf_dict)
    good_noun_tfidf_str = make_display_noun_tfidf_str(good_noun_count,
                                                      good_ordered_nouns,
                                                      good_ordered_tfidf)
    #グラフ画像の作成
    uninterested_scatter = gen_scatter_plot(uninterested_ordered_idf,
                                            uninterested_ordered_tfidf,
                                            uninterested_ordered_nouns,
                                            COLOR_RED,
                                            '「興味なし」と評価された記事内の語句で\n'\
                                            '影響の大きな語（TF-IDF上位30語）の散布図')
    #表示のための'名詞:TF-IDF値'のテキストを作成
    uninterested_noun_count = len(uninterested_noun_tfidf_dict)
    uninterested_noun_tfidf_str = make_display_noun_tfidf_str(
                                                        uninterested_noun_count,
                                                        uninterested_ordered_nouns,
                                                        uninterested_ordered_tfidf)
    context = {
        'good_scatter': good_scatter,
        'good_noun_tfidf': good_noun_tfidf_str,
        'uninterested_scatter': uninterested_scatter,
        'uninterested_noun_tfidf': uninterested_noun_tfidf_str
    }
    return render(request, 'app/graph.html', context)

def get_category_jp(category):
    """英語表記で受け取ったcategoryを日本語表記にして返す。"""
    return CATEGORY_DICT[category]

def get_category_en(category):
    """日本語表記で受け取ったカテゴリーを英語表記にして返す。"""
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

def make_ordered_values_lists(noun_tfidf_dict, noun_idf_dict):
    """IDF, TF-IDF, 名詞をそれぞれ同じ順番（TF-IDF降順）に並べて
    三つのリストとして返す。
    """
    #各単語ごとにtupleの組(idf, tfidf, noun)にしてtfidfの値でソートする
    values_tuple_list = []
    for noun, tfidf in noun_tfidf_dict.items():
        try:
            idf = noun_idf_dict[noun]
        except KeyError:
            continue
        values_tuple_list.append((float(idf), float(tfidf), noun))
    sorted_values = sorted(values_tuple_list,
                           key=operator.itemgetter(1),
                           reverse=True)
    #idf, tfidf, 名詞を順序を合わせてリストに格納する
    ordered_idf = []
    ordered_tfidf = []
    ordered_nouns = []
    for values_tuple in sorted_values:
        ordered_idf.append(values_tuple[0])
        ordered_tfidf.append(values_tuple[1])
        ordered_nouns.append(values_tuple[2])
    return ordered_idf, ordered_tfidf, ordered_nouns

def make_display_noun_tfidf_str(word_count, ordered_nouns, ordered_tfidf):
    """名詞、TF-IDF値を成形したテキストの形で返す。"""
    connection_count = word_count
    #単語をつなげる長さを決める
    if (DISPLAY_COUNT * 2) < word_count:
        connection_count = DISPLAY_COUNT * 2
    display_str = ''
    break_counter = 0
    #引数として受け取った名詞、TF-IDF値をつなげる
    for i in range(connection_count):
        display_str = display_str + ordered_nouns[i] + ': ' \
                            + str(round(ordered_tfidf[i], 3)) + \
                             ", &nbsp;&nbsp;&nbsp;&nbsp;"
        #５語つなぐごとに改行する
        break_counter += 1
        if 4 < break_counter:
            display_str += "<br>"
            break_counter = 0
    return display_str