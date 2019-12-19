from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^newsIntro/$', views.newsIntro, name="newsIntro"), #新闻栏目简介
    url(r'^newsColumn/(?P<columnSlug>[^/]+)/$', views.newsColumn, name="newsColumn"), #新闻列表
    url(r'^newsDetail/(?P<pk>\d+)/(?P<newsSlug>[^/]+)/$', views.newsDetail, name="newsDetail"), #新闻文章详情

    url(r'^recBookList/$', views.recBookList, name="recBookList"), #每周一书列表
    url(r'^recBookList/(?P<pk>\d+)/(?P<ISBN>[^/]+)/$', views.recBookDetail, name='recBookDetail'),

    url(r'^rankList/$', views.rankList, name="rankList"),  # 排行榜列表

    url(r'^newsSearch/$', views.newsSearch, name="newsSearch"),  # 新闻搜索结果
]