from django.urls import path
from articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_response, name='frame'),
    path('login', views.login_process, name='login'),
    path('guest', views.login_guest_user, name='guest'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_reopen, name='logout'),
    path('pages', views.left_frame, name='pages'),
    path('src_link', views.init_link, name='src_link'),
    path('loading', views.loading, name='loading'),
    path('result', views.result, name='result'),
    path('<str:clicked_category>', 
          views.article_link, name='src_link'),
    path('all_clear/<str:category_in_jp>',
          views.all_clear, name='all_clear'),
    path('eval_good/<str:clicked_category>/<str:article_title>', 
          views.eval_good, name='eval_good'),
    path('eval_uninterested/<str:clicked_category>/<str:article_title>', 
          views.eval_uninterested, name='eval_uninterested'),
]
