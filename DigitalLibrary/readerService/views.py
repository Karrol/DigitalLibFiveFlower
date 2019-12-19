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
    return render (request,'readerService/bookReservationTips.html')

def bookReservationBooked(request):
    bookResers = bookReser.objects.all()
    return render (request,'readerService/bookReservationBooked.html',{'bookResers':bookResers})

def borrowTips(request):
    return render (request,'readerService/borrowTips.html')

def compensation(request):
    return render (request,'readerService/compensation.html')

def cdInfo(request):
    return render (request,'readerService/cdInfo.html')

def renewal(request):
    return render (request,'readerService/renewal.html')

def cableNumber(request):
    redsertimes = RedSerTime.objects.all()
    return render(request, 'readerService/cableNumber.html', { 'redsertimes': redsertimes  })

def cd(request):
    return render (request,'readerService/cd.html')

def serviceTime(request):
    return render (request,'readerService/serviceTime.html')