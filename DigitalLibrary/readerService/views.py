from django.shortcuts import render


from .models import bookReser
from .models import RedSerTime

def bookReservation(request):
    if request.method=='GET':
        return render (request,'readerService/bookReservation.html')
    elif request.method=='POST':
        bookreser =bookReser()
        bookreser.readerId = request.POST.get('readerId')
        bookreser.book=request.POST.get('book')
        bookreser.bookId = request.POST.get('bookId')
        bookreser.returnTime = request.POST.get('returnTime')
        bookreser.place = request.POST.get('place')
        bookreser.save()
        return render (request,'readerService/success.html')

def bookReservationTips(request):
    bookreservationtips = RedSerTime.objects.all()
    return render(request, 'readerService/bookReservationTips.html', { 'bookreservationtips': bookreservationtips  })

def bookReservationBooked(request):
    bookResers = bookReser.objects.all()
    return render (request,'readerService/bookReservationBooked.html',{'bookResers':bookResers})

def borrowTips(request):
    borrowtips = RedSerTime.objects.all()
    return render(request, 'readerService/borrowTips.html', { 'borrowtips': borrowtips  })

def compensation(request):
    compensations = RedSerTime.objects.all()
    return render(request, 'readerService/compensation.html', { 'compensations': compensations  })

def cdInfo(request):
    cdinfos = RedSerTime.objects.all()
    return render(request, 'readerService/cdInfo.html', { 'cdinfos': cdinfos  })

def renewal(request):
    renewals = RedSerTime.objects.all()
    return render(request, 'readerService/renewal.html', { 'renewals': renewals  })

def cableNumber(request):
    cablenumbers = RedSerTime.objects.all()
    return render(request, 'readerService/cableNumber.html', { 'cablenumbers': cablenumbers  })

def cd(request):
    cds = RedSerTime.objects.all()
    return render(request, 'readerService/cd.html', { 'cds': cds  })

def serviceTime(request):
    servicetimes = RedSerTime.objects.all()
    return render(request, 'readerService/serviceTime.html', { 'servicetimes': servicetimes  })
