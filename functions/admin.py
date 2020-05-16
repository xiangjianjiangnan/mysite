from django.contrib import admin
from .models import ArticleComment
# Register your models here.


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('article','text','user','reply_to','parent','root','comment_time')
    search_fields = ('content_object', 'user', 'reply_to', 'comment_time')
admin.site.register(ArticleComment,ArticleCommentAdmin)