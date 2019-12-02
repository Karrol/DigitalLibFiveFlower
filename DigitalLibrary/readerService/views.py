from django.shortcuts import render

#from booktest.models import bookInfo

#def showBooks(request):
#    books = bookInfo.objects.all()
#    return render(request,'formanager/showBooks.html',{'books':books})

# Create your views here.

#新增一个帖子
from readerService.models import bookReser

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
    return render (request,'readerService/bookReservationBooked.html')

def borrowTips(request):
    return render (request,'readerService/borrowTips.html')

def compensation(request):
    return render (request,'readerService/compensation.html')

def cableNumber(request):
    return render (request,'readerService/cableNumber.html')

def cdInfo(request):
    return render (request,'readerService/cdInfo.html')

def renewal(request):
    return render (request,'readerService/renewal.html')

def serviceTime(request):
    return render (request,'readerService/serviceTime.html')

def cd(request):
    return render (request,'readerService/cd.html')
