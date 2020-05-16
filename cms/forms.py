from django import forms
# from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from django.contrib.auth import authenticate
# from django.core.cache import cache

class RecommendForm(forms.Form):
    recommend_type = forms.IntegerField()
    recommend_id = forms.CharField()
    recommend_text = forms.CharField()