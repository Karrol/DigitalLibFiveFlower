from django.conf.urls import url, include
from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    path('category/',views.libBrief, name = 'libBrief'),
    path('category/<str:categorySlug>/',views.serviceCategory, name='serviceCategory'),
    path('intro/<int:pk>/<str:serviceSlug>/', views.serviceDetail, name='serviceDetail'),
    path('serviceSearch/', views.serviceSearch, name="serviceSearch"),
]