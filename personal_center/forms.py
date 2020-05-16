from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from django.contrib.auth import authenticate
# from django.core.cache import cache

# 文章上传的表单验证
class ArticleReleaseForm(forms.Form):
    article_cover = forms.ImageField()#封面
    anthology = forms.CharField(max_length=20)#文选
    article_title = forms.CharField(max_length=50)#标题
    summary = forms.CharField(max_length=200)#摘要
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name='article_ckeditor'))#内容
    category = forms.CharField(max_length=20)#分类


# 文选上传的表单验证 
class AnthologyReleaseForm(forms.Form):
    anthology_title = forms.CharField()
    anthology_cover = forms.ImageField()
    anthology_describe = forms.CharField(widget=forms.Textarea)


# 这是修改个人信息的验证表单
class InformationForm(forms.Form):   
    email = forms.EmailField()
    autograph = forms.CharField()
    birthday = forms.DateField()
    sex = forms.CharField()
    telephone = forms.CharField(max_length=11)
    city = forms.CharField(max_length=20)

class PortraitForm(forms.Form):
    portrait = forms.ImageField()


class AhthologyChangeForm(forms.Form):
    anthology_id = forms.IntegerField()
    anthology_title = forms.CharField()
    anthology_cover = forms.ImageField(required=False)# 如果图片可以不上传，记得要加入括号中的参数
    anthology_describe = forms.CharField(widget=forms.Textarea)

# 文章上传的表单验证
class ArticleChangeForm(forms.Form):
    article_id = forms.IntegerField()
    article_cover = forms.ImageField(required=False)#封面
    anthology = forms.CharField(max_length=20)#文选
    article_title = forms.CharField(max_length=50)#标题
    summary = forms.CharField(max_length=200)#摘要
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name='article_ckeditor'))#内容
    category = forms.CharField(max_length=20)#分类