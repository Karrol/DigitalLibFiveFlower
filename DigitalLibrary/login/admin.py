from django.contrib import admin
from .models import Reader

admin.site.register(Reader)


admin.site.name = '图书馆信息管理'
admin.site.site_header = '图书馆信息管理'
