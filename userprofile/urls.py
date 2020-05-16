from django.urls import path
from . import views
import re

app_name = 'userprofile'

urlpatterns = [
    path('login/post/',views.user_login, name='user_login'),
    path('logout/',views.user_logout, name='user_logout'),
    path('register/post/',views.user_register, name='user_register'),
    path('captcha/',views.img_captcha,name='img_captcha'),
    path('login/',views.login_show, name='login_show'),
    path('register/',views.register_show, name='register_show'),
    path('reset_user/',views.reset_show, name='reset_show'),
    path('reset_code/',views.reset_code, name='reset_code'),
    path('reset_confirm/',views.reset_confirm, name='reset_confirm'),
    path('reset_pwd/',views.reset_pwd, name='reset_pwd'),
    path('pwd_show/',views.pwd_show, name='pwd_show'),
    # path('remind/',views.remind_show, name='remind_show'),
    path("reset_password/<slug:code>",views.remind_show, name='remind_show'),     
]


# Django默认支持以下5个转化器：

# str,匹配除了路径分隔符（/）之外的非空字符串，这是默认的形式
# int,匹配正整数，包含0。
# slug,匹配字母、数字以及横杠、下划线组成的字符串。
# uuid,匹配格式化的uuid，如 075194d3-6885-417e-a8a8-6c931e272f00。
# path,匹配任何非空字符串，包含了路径分隔符