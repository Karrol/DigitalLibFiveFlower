#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name='readerCenter'

urlpatterns = [
                #个人资料
                path('profile/', views.profile, name='profile'),
                #更改个人资料
                path('changeinfo/', views.readerChangeinfo, name='changeinfo'),
                path('uploadImg/', views.uploadImg, name='uploadImg'),
                #消息列表
                path('notice/', views.readerNotice, name='notice'),
                #消息详情
                path('shownotice/detail$', views.showNotice, name='noticeDetail'),
                #我的借阅
                path('bowrrowing', views.readerBorrowing, name='borrowingSituation'),
                #我的借阅页面读者的借还操作
                url(r'^book/action$', views.readerOperateBook, name='reader_operation'),
                #我的检索历史
                path('showsearchlist', views.show_mysearchlist, name='showsearchlist'),
                path('searchlist', views.add_to_searchlist, name='searchlist'),
                #我的图书馆
                path('mylib/', views.mylib, name='mylib'),
                path('mylib_del/<str:ISBN>/', views.mylib_del, name='mylib_del'),
                path('mylib_add/<str:ISBN>/', views.mylib_add, name='mylib_add'),
                path('mylib_search/', views.mylib_search, name='mylib_search'),

    
              ]
