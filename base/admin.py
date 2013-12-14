from django.contrib import admin
from models import *


class InfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'source_url', 'post_url', 'post_status', 'category')
    list_filter = ('post_status', 'category')


admin.site.register(G)
admin.site.register(Info, InfoAdmin)