from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^bookReservation/$', views.bookReservation, name='bookReservation'),
    url(r'^bookReservationTips/$', views.bookReservationTips, name='bookReservationTips'),
    url(r'^bookReservationBooked/$', views.bookReservationBooked, name='bookReservationBooked'),
    url(r'^borrowTips/$', views.borrowTips, name='borrowTips'),
    url(r'^compensation/$', views.compensation, name='compensation'),
    url(r'^cd/$', views.cd, name='cd'),
    url(r'^cableNumber/$', views.cableNumber, name='cableNumber'),
    url(r'^cdInfo/$', views.cdInfo, name='cdInfo'),
    url(r'^renewal/$', views.renewal, name='renewal'),
    url(r'^bookReser/$', views.bookReser, name='bookReser'),
    url(r'^serviceTime/(?P<RedserSlug>[^/]+)/$', views.serviceTime, name='serviceTime'),
]
