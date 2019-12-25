from django.conf.urls import url, include
from django.urls import path
from . import views

app_name = "infoCenter"

urlpatterns = [
    path('newsIntro/', views.newsIntro, name="newsIntro"), #新闻栏目简介
    path('newsColumn/<str:columnSlug>/', views.newsColumn, name="newsColumn"), #新闻列表
    path('newsDetail/', views.newsDetail, name="newsDetail"), #新闻文章详情

    path('recBookList/', views.recBookList, name="recBookList"), #每周一书列表
    path('recBookHis/', views.recBookDetail, name='recBookDetail'),

    path('rankList/', views.rankList, name="rankList"),  # 排行榜列表
    path('rankDetail/<int:rankID>/', views.rankDetail, name="rankDetail"), #排行榜详情

    path('toolDownload/', views.toolDownload, name="toolDownload"),  # 工具下载
    path('NoteExpress/', views.NoteExpress, name="NoteExpress"),  # NoteExpress下载
    path('EndNote/', views.EndNote, name="EndNote"),  # NoteExpress下载

    path('newsSearch/', views.newsSearch, name="newsSearch"),  # 新闻搜索结果
]