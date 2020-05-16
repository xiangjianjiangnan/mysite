from django.urls import path
from . import views

app_name = 'functions'

urlpatterns = [
    path('article_comment/',views.article_comment, name='article_comment'),
    path('article_like/',views.article_like, name='article_like'),
    path('articlecomment_like/',views.articlecomment_like, name='articlecomment_like'),
    path('article_collect/',views.article_collect, name='article_collect'),
    path('author_follow/',views.author_follow, name='author_follow'),
]