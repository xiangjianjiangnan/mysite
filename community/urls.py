from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('',views.community, name='community'),
    path('topic/<int:id>/',views.topic_detail, name='topic_detail'),
    path('topic_create',views.topic_create, name='topic_create'),
    path('topic_comment',views.topic_comment, name='topic_comment'),
    path('topic_comment_like',views.topic_comment_like, name='topic_comment_like'),
    path('category=<str:category>',views.topic_categry, name='topic_categry'),
    path('topic_search',views.topic_search, name='topic_search'),
]