import re
from django.test.client import RequestFactory
from articles.models import Preference, User

def get_test_user():
    test_username = 'test_user'
    test_user = None
    if User.objects.filter(username=test_username).exists():
        test_user = User.objects.get(username=test_username)
    else:
        test_user = User.objects.create_user(username=test_username)
    return test_user

def create_user_with_password():
    test_username = 'password_user'
    test_password = 'valid_test_password'
    return User.objects.create_user(username=test_username, password=test_password)

def get_request(url_path):
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
    request_factory = RequestFactory()
    return request_factory.post(path=path, data=data)


def get_request_with_pref(url_path):
    request = get_request(url_path)
    user = request.user
    if not Preference.objects.filter(username=user).exists():
        Preference.objects.create(username=user)
    return request

def create_test_preference(user):
    if not Preference.objects.filter(username=user).exists():
        Preference.objects.create(username=user)

def remove_csrf(html_source):
    """csrf部分を除去して返す関数"""
    csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
    return re.sub(csrf_regex, '', html_source)

# def load_template_tag(tag_str, context=None):
#     """テンプレートタグを読み出して返す関数"""
#     context = context or {}
#     context = Context(context)
#     return Template(tag_str).render(context)