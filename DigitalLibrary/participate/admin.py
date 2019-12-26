from django.contrib import admin
# 别忘了导入ArticlerPost
from .models import ArticlePost ,RecbooklistInfo, ContactInfo, Comment

# 导入文章栏目
from .models import ArticleColumn

# Register your models here.
# 注册ArticlePost到admin中
admin.site.register(ArticlePost)

# 注册文章栏目
admin.site.register(ArticleColumn)
# 注册推荐图书列表
admin.site.register(RecbooklistInfo)
# 注册馆员联系信息
admin.site.register(ContactInfo)
# 注册评论
admin.site.register(Comment)
