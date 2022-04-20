from django.urls import path
from articles import views

app_name = 'articles'

urlpatterns = [
    path('', views.frame, name='frame'),
    path('login', views.login_process, name='login'),
    path('guest', views.login_guest_user, name='guest'),
    path('signup', views.signup, name='signup'),
    path('signup_completed', views.signup_completed, name='signup_completed'),
    path('logout', views.logout_reopen, name='logout'),
    path('pages', views.left_frame, name='pages'),
    path('src_link', views.article_link, name='src_link'),
    path('src_link/<str:clicked_category>', views.article_link, name='src_link'),
    path('loading', views.loading, name='loading'),
    path('call_apply_choices', views.call_apply_choices, name='call_apply_choices'),
    path('result_positive', views.result_positive, name='result_positive'),
    path('result_negative', views.result_negative, name='result_negative'),
    path('all_clear', views.all_clear, name='all_clear'),
    path('category_clear/<str:category_in_jp>',
          views.category_clear, name='category_clear'),
    path('eval_good/<str:clicked_category>/<str:article_title>', 
          views.eval_good, name='eval_good'),
    path('eval_uninterested/<str:clicked_category>/<str:article_title>', 
          views.eval_uninterested, name='eval_uninterested'),
]
