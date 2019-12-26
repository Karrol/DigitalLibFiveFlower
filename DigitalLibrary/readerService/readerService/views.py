from django.shortcuts import render

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import bookReser
from .models import RedSerTime
from .models import lectureReser
from .models import CD

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
    # 实现搜索
    q = request.GET.get('q')
    all_cds = CD.objects.all()
    cdlist = []
    # 如果前端传入关键字，才会进行检索，否则显示全部买家
    if q:
        for cd in all_cds:
            if q in cd.title:
                cdlist.append(cd)
        all_cds = cdlist
    if all_cds:
        paginator = Paginator(all_cds, 10)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        context = {
            'contacts':contacts,
        }
        return render(request, 'readerService/cd.html', context)
    else:
        info = '暂无数据'
        return render(request, 'readerService/cd.html', {'info': info})

'''
def cd(request):
        # 实现搜索
        q = request.GET.get('q')
        all_cds = CD.objects.all()
        cdlist = []
        # 如果前端传入关键字，才会进行检索，否则显示全部买家
        if q:
            for cd in all_cds:
                if q in cd.title:
                    cdlist.append(cd)
            all_cds = cdlist
            return render(request, 'readerService/cd.html', {'all_cds':all_cds})

        current_path = request.get_full_path()

        # 翻页功能实现
        paginator = Paginator(all_cds, 5)
        pindex = request.GET.get('page', 1)

        try:
            # page是paginator实例对象的方法，返回第page页的实例对象，所以books是第page页的记录集
            pbooks = paginator.page(pindex)
        except PageNotAnInteger:
            pbooks = paginator.page(1)
        except EmptyPage:
            pbooks = paginator.page(paginator.num_pages)

        # ugly solution for &page=2&page=3&page=4
        # 当你已经是某一页时，current_path的最后有&page(previous),所以这里是在做清洗
        if '?page' in current_path:
            current_path = current_path.split('?page')[0]

        context = {
            'pbooks': pbooks,
            'current_path': current_path,
        }
        return render(request, 'readerService/cd.html', context)
'''

def serviceTime(request):
    servicetimes = RedSerTime.objects.all()
    return render(request, 'readerService/serviceTime.html', { 'servicetimes': servicetimes  })

def lecture(request):
    return render(request, 'readerService/lecture.html')

def lectureBook(request):
    if request.method=='GET':
        return render (request,'readerService/lectureBook.html')
    elif request.method=='POST':
        lecturereser =lectureReser()
        lecturereser.readerId = request.POST.get('readerId')
        lecturereser.email=request.POST.get('email')
        lecturereser.lectureName = request.POST.get('lectureName')
        lecturereser.speaker = request.POST.get('speaker')
        lecturereser.lectureTime = request.POST.get('lectureTime')
        lecturereser.save()
        return render (request,'readerService/success.html')

def lectureTips(request):
    return render(request, 'readerService/lectureTips.html')

