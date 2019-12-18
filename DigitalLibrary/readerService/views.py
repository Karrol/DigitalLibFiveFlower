from django.shortcuts import render


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

def cd(request):
    return render (request,'readerService/cd.html')

def serviceTime(request, RedserSlug, pk):
    redservice = RedSer.objects.get(pk=pk)

    if RedserSlug != redservice.RedserSlug:
        return redirect(redservice, permanent=True)

    return render(request, 'readerService/serviceTime.html', {
        'redsertime': redsertime
    })