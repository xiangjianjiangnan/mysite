from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    # path('',views.article, name='article'),
    # path('article_list/',views.article_list, name='article_list'), 
    path('article_serach/',views.article_serach, name='article_serach'),
    path('<int:id>/',views.article_detail, name='article_detail'),
]