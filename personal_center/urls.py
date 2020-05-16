from django.urls import path
from . import views

app_name = 'personal_center'

urlpatterns = [
    path('',views.personal_center_home, name='personal_center_home'),
    path('article_release/',views.article_release, name='article_release'),
    path('article_create/',views.article_create, name='article_create'),
    path('tag_release/',views.tag_release, name='tag_release'),
    path('anthology_release/',views.anthology_release, name='anthology_release'),
    path('anthology_create/',views.anthology_create, name='anthology_create'),
    path('anthology/<int:id>/',views.anthology_article, name='anthology_article'),
    path('p_<int:id>',views.public_author_message, name='public_author_message'),
    path('author_follow',views.author_follow, name='author_follow'),
    path('message_center',views.message_center, name='message_center'),
    path('information',views.information, name='information'),
    path('information_change/',views.information_change, name='information_change'),
    path('portrait_change/',views.portrait_change, name='portrait_change'),
    path('topics/',views.topic_show, name='topic_show'),
    path('anthology_delete/',views.anthology_delete, name='anthology_delete'),
    path('anthology_change/',views.anthology_change, name='anthology_change'),
    path('anthology_revise/',views.anthology_change_handle, name='anthology_change_handle'),
    path('article_delete/',views.article_delete, name='article_delete'),
    path('article_change/',views.article_change, name='article_change'),
    path('article_revise/',views.article_change_handle, name='article_change_handle'),
    path('follows/',views.follow_show, name='follow_show'),
    path('fans/',views.fans_show, name='fans_show'),
    path('p_<int:id>/anthologys',views.public_author_anthologys, name='public_author_anthologys'),
    path('anthology_<int:id>/articles',views.public_author_articles, name='public_author_articles'),
    path('p_<int:id>/follows',views.public_author_follows, name='public_author_follows'),
    path('p_<int:id>/fans',views.public_author_fans, name='public_author_fans'),
]