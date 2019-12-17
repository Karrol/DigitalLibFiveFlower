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

    # 发表评论
    path('postComment/<int:article_id>/', views.post_comment, name='post_comment'),

    # 捐赠须知
    path('donationRules/', views.donation_rules, name='donation_rules'),
    # 捐赠处理
    path('donationTreatments/', views.donation_treatments, name='donation_treatments'),
    # 联系方式
    path('donationContact/', views.donation_contact, name='donation_contact'),

    # 图书推荐
    path('bookRecom/', views.book_recom, name='book_recommendation'),

    # 读者推荐列表
    path('bookRecList/', views.recom_list, name='bookrec_list'),
]