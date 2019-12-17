#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,re_path
from . import views

app_name='search'

urlpatterns = [
                #检索首页
                path('searchindex/', views.index, name='searchindex'),
                #检索结果页
                path('searchBook/', views.book_search, name='searchBook'),
                #操作检索结果
                #re_path(r'^app01/books/(\d+)/delete',views.del_book,name='delete'),
                #图书详情
                path('bookDetail/<str:ISBN>/', views.book_detail, name='bookDetail'),
    
              ]
