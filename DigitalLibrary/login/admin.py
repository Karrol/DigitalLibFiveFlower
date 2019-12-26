from django.contrib import admin
from .models import Reader,librarian_info
from django.contrib.auth.models import User

admin.site.register(Reader)
admin.site.register(librarian_info)



admin.site.name = '图书馆信息管理'
admin.site.site_header = '图书馆信息管理'
