from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('',views.home, name='home'),
    path('news/<str:category>',views.news, name='news'),
    path('category=<str:category>',views.category, name='category'),
    path('service/government/',views.service_government, name='service_government'),
    path('service/media/',views.service_media, name='service_media'),
    path('service/intelligence/',views.service_intelligence, name='service_intelligence'),
    path('service/company/',views.service_company, name='service_company'),
]