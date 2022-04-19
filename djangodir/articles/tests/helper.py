import re
from django.test.client import RequestFactory
from articles.models import Preference, User

def get_test_user():
    """'test_user'というusernameのUserインスタンスを返す関数。
    パスワードは設定されていない。既に存在する場合はそれを返す。
    """
    test_username = 'test_user'
    test_user = None
    if User.objects.filter(username=test_username).exists():
        test_user = User.objects.get(username=test_username)
    else:
        test_user = User.objects.create_user(username=test_username)
    return test_user

def create_user_with_password():
    """パスワード有りのUserインスタンスを生成する関数。"""
    test_username = 'password_user'
    test_password = 'valid_test_password'
    return User.objects.create_user(username=test_username, password=test_password)

def get_request(url_path):
    """引数として受け取った'url_path'へのリクエスト(GET)を返す関数。
    Userとして'test_user'を持つ。"""
    test_username = 'test_user'
    test_user = None
    if User.objects.filter(username=test_username).exists():
        test_user = User.objects.get(username=test_username)
    else:
        test_user = User.objects.create_user(username=test_username)
    request_factory = RequestFactory()
    request = request_factory.get(url_path)
    request.user = test_user
    return request

def post_request_with_anonymous(path, data):
    """引数として受け取った'url_path'へのリクエスト(POST)を返す関数。"""
    request_factory = RequestFactory()
    return request_factory.post(path=path, data=data)


def get_request_with_pref(url_path):
    """引数として受け取った'url_path'へのリクエスト(GET)を返す関数。
    Userとして'test_user'を持ち、そのUserのPreferenceも作成する。"""
    request = get_request(url_path)
    user = request.user
    if not Preference.objects.filter(user=user).exists():
        Preference.objects.create(user=user)
    return request

def prepare_user_pref(testcase):
    """ログイン状態のUser'test_user'を用意し、そのUserのPreferenceを作成する"""
    user = get_test_user()
    testcase.client.force_login(user)
    create_test_preference(user)

def create_test_preference(user):
    """引数として受け取ったUserのPreferenceを作成する。
    既にある場合は何もしない。
    """
    if not Preference.objects.filter(user=user).exists():
        Preference.objects.create(user=user)

def remove_csrf(html_source):
    """csrf部分を除去して返す関数"""
    csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
    return re.sub(csrf_regex, '', html_source)
