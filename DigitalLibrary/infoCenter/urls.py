from django.conf.urls import url, include
from django.urls import path
from . import views

app_name = "infoCenter"

urlpatterns = [
    path('newsIntro/', views.newsIntro, name="newsIntro"), #新闻栏目简介
    path('newsColumn/<str:columnSlug>/', views.newsColumn, name="newsColumn"), #新闻列表
    path('newsDetail/<int:pk>/<str:newsSlug>/', views.newsDetail, name="newsDetail"), #新闻文章详情

    path('recBookList/', views.recBookList, name="recBookList"), #每周一书列表
    path('recBookList/<int:pk>/<str:recID>/', views.recBookDetail, name='recBookDetail'),

    path('rankList/', views.rankList, name="rankList"),  # 排行榜列表

    path('newsSearch/', views.newsSearch, name="newsSearch"),  # 新闻搜索结果
]