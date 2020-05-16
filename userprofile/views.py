from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.cache import cache
from django.urls import reverse
from .forms import LoginForm,RegisterForm,ResetUserForm,ResetConfirmForm,ResetPwdForm
from utils.captcha.captcha import Captcha
from utils.random.random import get_random_code
from io import BytesIO
from article.models import Anthology
from mysite import settings
from django.core.mail import send_mail
from functions.models import EmailVerify
import datetime
import pandas as pd

def remind_show(request,code):
    context = {}
    message = '请尽快前往您的邮箱进行激活，否则无法登录'
    context['message'] = message
    return render(request, 'remind.html', context)



# 只能在未登录状态下访问的装饰器，和login_required相反
def anonymous_required(function=None, redirect_url=None):
   if not redirect_url:
       redirect_url = settings.LOGIN_REDIRECT_URL

   actual_decorator = user_passes_test(
       lambda u: u.is_anonymous,
       login_url=redirect_url
   )
   if function:
       return actual_decorator(function)
   return actual_decorator




# 注册页面展示
@anonymous_required
def register_show(request):
    context = {}
    message = '欢迎注册！'
    context['message'] = message
    return render(request, 'register.html', context)

# 用户注册
@anonymous_required
@require_POST
def user_register(request):
    context = {}
    referer = request.META.get('HTTP_REFERER')
    user_register_form = RegisterForm(request.POST)
    if user_register_form.is_valid():
        register_username = user_register_form.cleaned_data['register_username']
        register_email = user_register_form.cleaned_data['register_email']
        register_password = user_register_form.cleaned_data['register_password']
        register_password2 = user_register_form.cleaned_data['register_password2']
        if register_password == register_password2:
            same_name_user = User.objects.filter(username=register_username)
            same_email_user = User.objects.filter(email=register_email)
            if same_name_user:
                message = '用户名已被注册！'
                context['message'] = message
                return render(request, 'register.html', context)
            elif same_email_user:
                message = '该邮箱已被注册！'
                context['message'] = message
                return render(request, 'register.html', context)
            else:
                register_user = User.objects.create(username=register_username,email=register_email)
                register_user.set_password(register_password)
                
                anthology = Anthology.objects.create(author=register_user)
                anthology.save()
                register_user.save()
                
                login(request,register_user)
                return render(request, 'home.html')
        else:
            message = '两次密码输入不一致'
            context['message'] = message
            return render(request, 'register.html', context)
    else:
        user_register_form = RegisterForm()
    return redirect(referer)




# 登录界面展示
@anonymous_required
def login_show(request):
    context = {}
    message = '欢迎登录！'
    context['message'] = message
    return render(request, 'login.html', context)


# 用户登录
#限定接收的请求必须为post请求
@require_POST
@anonymous_required
def user_login(request):
    context = {}
    referer = request.META.get('HTTP_REFERER',reverse('public:home'))
    user_login_form = LoginForm(request.POST)
    if user_login_form.is_valid():
        remember = user_login_form.cleaned_data['remember']
        username = user_login_form.cleaned_data['username']
        password = user_login_form.cleaned_data['password']
        img_captcha = user_login_form.cleaned_data['img_captcha']
        cached_img_captcha = cache.get(img_captcha.lower())
        if not cached_img_captcha or cached_img_captcha.lower() != img_captcha.lower():
            message = '图形验证码错误！'
            context['message'] = message
            return render(request, 'login.html', context)
        user = authenticate(username=username, password=password)
        if user is None:
            message = '账号或密码错误！'
            context['message'] = message
            return render(request, 'login.html', context)
        login(request, user)
        if remember:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)       
        if 'next=' in referer: 
            # homeurl = 'http://127.0.0.1:8000'
            nextindex = referer.index('next=') + 5
            nexturl =  referer[nextindex:]
            # print("跳转链接是：")
            # print(nexturl)
            return redirect(nexturl)
           
        else:
            return redirect("public:home")
    else:
        user_login_form = LoginForm()
        return redirect(referer)

# 用户退出
def user_logout(request):
    referer = request.META.get('HTTP_REFERER')
    logout(request)
    return redirect(referer)
    # return render(request,'home.html')
    

# 忘记密码用户确认页面展示
@anonymous_required
def reset_show(request):
    context = {}
    message = '填写用户'
    context['message'] = message
    return render(request, 'reset_user.html', context)

# 根据用户填写的用户名和邮箱，进行寻找该用户
@anonymous_required
def reset_code(request):
    context = {}
    resetuser_form = ResetUserForm(request.POST)
    if resetuser_form.is_valid():
        reset_username = resetuser_form.cleaned_data['reset_username']
        reset_email = resetuser_form.cleaned_data['reset_email']

        user = get_object_or_404(User,username=reset_username,email=reset_email)
        if user:
            # 如果该用户存在，那么就向该用户的邮箱中发送一个8位的验证码，并保存在数据库中
            code = get_random_code(8)
            # 在数据库中查找或者创建一条信息，并将它的验证码更改，这样，每一个用户的每一种类型只会存在一个，不会浪费存储资源。
            email_verifycode, created = EmailVerify.objects.get_or_create(email=user.email, send_type='2')
            email_verifycode.code = code
            email_verifycode.save()
            # 接下来就是向该用户的用邮箱中发送这个八位的验证码
            email_title = '【CosData网】重置密码'
            email_text = '您正在【CosData网】执行找回密码操作，请妥善保管好您的验证码，以防账号安全问题，您的验证码为：' + code
            email_form = settings.EMAIL_FROM
            email_to = [user.email]
            send_mail(email_title,email_text,email_form,email_to)
            message = '身份确认，验证码有效期：10分钟'
            context['message'] = message
            context['email'] = reset_email
            # 携带者用户邮箱字段，跳转到下一个页面，让其填写发送的验证码
            return render(request, 'reset_code.html', context)
        else:
            # 如果该用户不存在那么返回忘记密码的那个页面
            message = '账号或邮箱不正确，请重新输入'
            context['message'] = message
            return render(request, 'reset_user.html', context)

# 将用户输入的验证码和数据库中的验证码进行比对
@anonymous_required
def reset_confirm(request):
    context = {}
    resetconfirm_form = ResetConfirmForm(request.POST)
    if resetconfirm_form.is_valid():
        confirm_email = resetconfirm_form.cleaned_data['confirm_email']
        confirm_code = resetconfirm_form.cleaned_data['confirm_code']
        # 现在已经得知用户的邮箱，在数据库中找到这条验证码记录，与输入的验证码进行比较，如果一致就进入到更改密码的页面
        email_verify = EmailVerify.objects.get(email=confirm_email, send_type='2')
        if email_verify:
            now_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            post_time = email_verify.post_time.strftime('%Y/%m/%d %H:%M:%S')
            # 利用pandas将字符串变为时间格式，求出时间差，因为数据库中的时间早了八个小时，所以要减掉
            seconds = (pd.to_datetime(now_time) - pd.to_datetime(post_time)).total_seconds() - 8*3600
            minutes = seconds/60
            # 如果提交的时间在10分钟的有效期内，就进行下一步的重置密码操作
            if minutes <= 10:
                message = '重置密码'
                context['message'] = message
                context['email'] = email_verify.email
                return render(request, 'reset_pwd.html', context)
            # 如果提交时间，超出10分钟的有效期，那么就要回到重新获取验证码的阶段   
            else:
                message = '验证码已过期，请重新获取验证码'
                context['message'] = message
                return render(request, 'reset_user.html', context)

# 重置新密码和确认密码，如果两个密码相同，则将该用户的密码进行重置，并且跳转到登录界面
@anonymous_required
def reset_pwd(request):
    context = {}
    resetpwd_form = ResetPwdForm(request.POST)
    if resetpwd_form.is_valid():
        reset_email = resetpwd_form.cleaned_data['reset_email']
        reset_pwd = resetpwd_form.cleaned_data['reset_pwd']
        reset_pwd2 = resetpwd_form.cleaned_data['reset_pwd2']
        # 根据邮箱找到该用户，如果用户存在那么就将两个密码进行对比
        if reset_pwd == reset_pwd2:
            user = User.objects.get(email=reset_email)
            user.set_password(reset_pwd)
            user.save()
            message = '重置密码成功！'
            context['message'] = message
            context['jump_to'] = "/user/login/"
            context['operation'] = "密码重置成功"
            return render(request, 'reset_sucess.html', context)
        else:
            message = '两次密码输入不一致'
            context['message'] = message
            context['email'] = email_verify.email
            return render(request, 'reset_pwd.html', context)

@anonymous_required
def pwd_show(request):
    context = {}
    message = '重置密码成功！'
    context['message'] = message
    context['operation'] = "密码重置成功"
    return render(request, 'reset_sucess.html', context)



def img_captcha(request):
    text,image = Captcha.gene_code()
    # BytesIO相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out,'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()
    cache.set(text.lower(),text.lower(),5*60)
    return response


# 用户找回密码功能
# def retrieve_pwd(request):
#     send_mail(
#         ''
#     )