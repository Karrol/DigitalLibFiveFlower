from django.urls import path,include
from readerService import views
app_name='readerService'

urlpatterns = [
    path('bookReservation/',views.bookReservation, name='bookReservation'),
    path('bookReservationTips/',views.bookReservationTips, name='bookReservationTips'),
    path('bookReservationBooked/',views.bookReservationBooked, name='bookReservationBooked'),
    path('borrowTips/',views.borrowTips, name='borrowTips'),
    path('compensation/',views.compensation, name='compensation'),
    path('cd/',views.cd, name='cd'),
    path('cableNumber/', views.cableNumber, name='cableNumber'),
    path('cdInfo/', views.cdInfo, name='cdInfo'),
    path('renewal/', views.renewal, name='renewal'),
    path('serviceTime/', views.serviceTime, name='serviceTime'),
    path('bookReser$',views.bookReservationBooked)
]
