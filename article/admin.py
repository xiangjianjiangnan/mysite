from django.contrib import admin
from .models import Article,Anthology,ReaderNum


class AnthologyAdmin(admin.ModelAdmin):
    list_display = ('id','anthology_title','author','created_time')
    search_fields = ('author','created_time')
admin.site.register(Anthology,AnthologyAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('article_title','category','anthology','author','created_time','update_time','read_num','is_active','is_pay','need_pay')
    search_fields = ('category', 'anthology', 'author', 'created_time')
admin.site.register(Article,ArticleAdmin)


class ArticleNumAdmin(admin.ModelAdmin):
    list_display = ('article','reader','once_read_time','more_read_time')
    search_fields = ('article','reader')
admin.site.register(ReaderNum,ArticleNumAdmin)