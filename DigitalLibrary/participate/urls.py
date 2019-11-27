# 引入path
from django.urls import path

# 引入views.py
from . import views

# 正在部署的应用的名称
app_name = 'participate'

urlpatterns = [
    # path函数将url映射到视图
    # 文章列表
    path('articleList/', views.article_list, name='article_list'),

     # 文章详情
    path('articleDetail/<int:id>/', views.article_detail, name='article_detail'),

    # 写文章
    path('articleCreate/', views.article_create, name='article_create'),

    # 删除文章
    path('articleDelete/<int:id>/', views.article_delete, name='article_delete'),

    # 安全删除文章
    path(
        'article-safe-delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),

    # 更新文章
    path('articleUpdate/<int:id>/', views.article_update, name='article_update'),
]