"""DigitalLibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

#import login.views as login_view
import readerCenter.views as readerCenter_view
import search.views as search_view
import participate.views as participate_view
import readerService.views as readerService_view
import librarian.views as librarian_view
import service.views as service_view
import infoCenter.views as infoCenter_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', librarian_view.index),
    path(r'index', librarian_view.index),
    path(r'login', include('login.urls')),
    path(r'readerCenter', include('readerCenter.urls')),
    path(r'search', include('search.urls')),
    path(r'participate', include('participate.urls')),
    path(r'readerService', include('readerService.urls')),
    path(r'librarian', include('librarian.urls')),
    path(r'service', include('service.urls')),
    path(r'infoCenter', include('infoCenter.urls')),
]
