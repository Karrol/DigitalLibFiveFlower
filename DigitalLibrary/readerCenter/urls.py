#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
                #个人资料
                path('profile/', views.profile, name='profile'),
                #更改个人资料
                path('changeinfo/', views.readerChangeinfo, name='changeinfo'),
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
                #检索历史的增删查改
                path('searchlist', views.add_to_searchlist, name='searchlist'),
                #我的图书馆
                path('mylib/', views.mylib, name='mylib'),

    
              ]
