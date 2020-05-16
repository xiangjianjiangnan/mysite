from django import forms

class ArticleCommentForm(forms.Form):
    article_id = forms.IntegerField()
    text = forms.CharField()
    reply_comment_id = forms.IntegerField()


