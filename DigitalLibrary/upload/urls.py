from django.conf.urls import url
from django.urls import path,include
from .views import *

app_name = 'upload'

urlpatterns = [
	url(r'upload_views',upload_views, name='upload_views'),
	#path('', index),
	path('index/', index,name='index'),  # 一个分片上传后被调用
    path('success/', upload_success),  # 所有分片上传成功后被调用
    path('file_exist/',list_exist),  # 判断文件的分片是否存在
	url(r'wother',wother_views,name='wother'),
	url(r'other',other_views,name='other'),
	url(r'open',open_views,name='open'),
	]
