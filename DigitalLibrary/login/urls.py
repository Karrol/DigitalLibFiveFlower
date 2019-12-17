from django.conf.urls import url
from django.contrib.staticfiles import views as static_views
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.urls import path

app_name ='login'

urlpatterns = [
                  #读者登录
                  path('rlogin/', views.reader_login, name='readerLogin'),
                  #馆员登录
                  path('liblogin/', views.librarian_login, name='librarianLogin'),
                  #登出
                  path('logout/', views.user_logout, name='user_logout'),
                  #注册
                  path('register/', views.user_register, name='userRegister'),
                  #修改密码
                  path('set_password/', views.set_password, name='set_password'),
    
              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
