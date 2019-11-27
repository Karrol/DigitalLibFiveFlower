from django.contrib import admin
# 别忘了导入ArticlerPost
from .models import ArticlePost

# 导入文章栏目
from .models import ArticleColumn

# Register your models here.
# 注册ArticlePost到admin中
admin.site.register(ArticlePost)

# 注册文章栏目
admin.site.register(ArticleColumn)
