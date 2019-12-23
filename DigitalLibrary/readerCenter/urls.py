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
                path('shownotice/', views.showNotice, name='noticeDetail'),
                #我的借阅
                path('bowrrowing/', views.readerBorrowing, name='borrowingSituation'),
                path('borrowHis/', views.readerBorrowHis, name='borrowHis'),
                path('moneyTask/', views.readerMoneyTask, name='moneyTask'),
                #我的借阅页面读者的借还操作
                url(r'^operatebook/', views.readerOperateBook, name='reader_operation'),
                #我的检索历史
                path('searchlist/', views.mysearchhis_show, name='showsearchlist'),
                path('searchlist_add/<str:ISBN>/', views.mysearchhis_add, name='mysearchhis_add'),
                path('searchlist_multi_add/', views.mysearchhis_multiadd, name='mysearchhis_multi_add'),
                path('searchlist_del/<str:ISBN>/', views.mysearchhis_del, name='mysearchhis_del'),
                path('searchlist_multi_del/', views.mysearchhis_multidel, name='mysearchhis_multi_del'),
                #我的图书馆
                path('mylib/', views.mylib, name='mylib'),
                path('mylib_del/<str:ISBN>/', views.mylib_del, name='mylib_del'),
                path('mylib_add/<str:ISBN>/', views.mylib_add, name='mylib_add'),
                path('mylib_multi_add/', views.mylib_multiadd, name='mylib_multi_add'),
                path('mylib_search/', views.mylib_search, name='mylib_search'),
                #用户常用快速链接入口
                path('quickLink/', views.quickLink, name='quickLink'),
                #用户对搜索系统提出的建议
                path('searchAdvice/', views.adviceSearch, name='searchAdvice'),

    
              ]
