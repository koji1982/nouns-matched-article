from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.article_response, name='frame'),
    path('pages.html', views.left_frame, name='pages'),
    # path('src_link.html', views.right_frame, name='src_link')
    path('src_link.html', views.init_link, name='src_link'),
    path('<str:clicked_category>src_link.html', views.article_link, name='src_link')
]
