#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
                #检索首页
                path('searchindex/(?P<int:ISBN>)', views.index, name='searchindex'),
                #检索结果页
                path('searchBook/', views.book_search, name='searchBook'),
                #图书详情
                path('bookDetail/', views.book_detail, name='bookDetail'),
                 
    
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
