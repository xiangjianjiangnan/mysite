from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('',views.cms, name='cms'),
    path('recommend/',views.recommend, name='recommend'),
    path('recommend_post/',views.recommend_post, name='recommend_post'),
]