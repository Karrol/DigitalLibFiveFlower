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
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', search_view.test, name='indextest'),
    url(r'^login/', include('login.urls',namespace = 'login')),
    url(r'^readerCenter/', include('readerCenter.urls',namespace = 'readerCenter')),
    url(r'^search/', include('search.urls',namespace = 'search')),
    url(r'^participate/', include('participate.urls')),
    url(r'^readerService/', include('readerService.urls')),
    url(r'^librarian/', include('librarian.urls')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^infoCenter/', include('infoCenter.urls')),
    url(r'^service/', include('service.urls')),
    #张丽：登录图形验证码
    url(r'^captcha', include('captcha.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
