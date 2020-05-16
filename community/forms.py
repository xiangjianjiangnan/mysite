from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from django.contrib.auth import authenticate
# from django.core.cache import cache

# 登录表单的验证
class TopicCreateForm(forms.Form):
    topic_title = forms.CharField(max_length=50)#文选
    category = forms.CharField(max_length=20)#分类
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name='topic_ckeditor'))#内容


class TopicCommentForm(forms.Form):
    topic_id = forms.IntegerField()
    reply_comment_id = forms.IntegerField()
    content = forms.CharField(widget=CKEditorUploadingWidget(config_name='topic_ckeditor'))#内容