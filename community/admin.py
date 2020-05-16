from django.contrib import admin
from .models import Topic


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id','topic_title','category','author','read_num','created_time')
    search_fields = ('author','category')
admin.site.register(Topic,TopicAdmin)