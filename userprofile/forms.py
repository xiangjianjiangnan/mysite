from django import forms
from django.contrib.auth import authenticate
from django.core.cache import cache

# 登录表单的验证
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50,min_length=6)
    remember = forms.IntegerField(required=False)
    img_captcha = forms.CharField(max_length=4,min_length=4)



# 用户注册表单
class RegisterForm(forms.Form):
    register_username = forms.CharField(max_length=50)
    register_email = forms.EmailField()
    register_password = forms.CharField(max_length=50,min_length=6)
    register_password2 = forms.CharField(max_length=50,min_length=6)


# 重置密码时，用户名和用邮箱的提交
class ResetUserForm(forms.Form):
    reset_username = forms.CharField(max_length=50)
    reset_email = forms.EmailField()

# 充值密码时，用户邮箱和验证码的提交
class ResetConfirmForm(forms.Form):
    confirm_email = forms.EmailField()
    confirm_code = forms.CharField(max_length=20)

# 重置密码和确认密码
class ResetPwdForm(forms.Form):
    reset_email = forms.EmailField()
    reset_pwd = forms.CharField(max_length=50,min_length=6)
    reset_pwd2 = forms.CharField(max_length=50,min_length=6)