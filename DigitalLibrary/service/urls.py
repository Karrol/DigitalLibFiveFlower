from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^category/$',views.libBrief, name = 'libBrief'),
    url(r'^category/(?P<categorySlug>[^/]+)/$',views.serviceCategory, name='serviceCategory'),
    url(r'^intro/(?P<pk>\d+)/(?P<serviceSlug>[^/]+)/$', views.serviceDetail, name='serviceDetail'),
]