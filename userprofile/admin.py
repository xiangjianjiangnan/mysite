from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('uid','user','sex','city','is_vip')
    # search_fields = ('author','created_time')
admin.site.register(Profile,ProfileAdmin)
