from django.conf.urls import url
from django.contrib.staticfiles import views as static_views
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import path

app_name='login'

urlpatterns = [
                  #登录
                  path('login/', views.user_login, name='login'),
                  #登出
                  path('logout/', views.user_logout, name='user_logout'),
                  #注册
                  path('register/', views.user_register, name='user_register'),
                  #修改密码
                  path('set_password/', views.set_password, name='set_password'),
    
              ]
