from django.shortcuts import render,redirect
from django.http import  HttpResponse
#from librarian.models import bookborrow_info,bookback_info, reader_info
from login.models import Reader, readerType ,librarian_info
from search.models import ebook_info ,bookEntity_info , bookshelf_info, booktype_info
from readerCenter.models import Borrowing
from readerService.models import CD,bookReser
from . import forms
import hashlib
from django.contrib.auth.models import User

# Create your views here.
import requests
def hash_code(s, salt='mysite'):#
    h = hashlib.sha256()
    s += salt
    h.update(s.encode()) # update方法只接收bytes类型
    return h.hexdigest()


def index(request):
    #张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user=request.user
        librarian=librarian_info.filter(user=user)
        if librarian:
            return render(request,'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')
    
    """url = 'http://127.0.0.1:8000/media/install.md'
    r = requests.get('http://127.0.0.1:8012/onlinePreview?url='+(url))
    text = r.text.replace('<link rel="stylesheet" href="','<link rel="stylesheet" href="http://49.235.21.24:8012/')
    text = text.replace('<script src="','<script src="http://49.235.21.24:8012/')
    #text = text.replace('url = url + "&officePreviewType="+previewType;','url = "http://127.0.0.1:8012/onlinePreview?url={}" + "&officePreviewType="+previewType;'.format(url))
    text = text.replace('url = window.location.href','url = "http://49.235.21.24:8012/onlinePreview?url={}" '.format(url))
    return HttpResponse(text)"""

def librarian_book(request):
    # 张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user = request.user
        librarian = librarian_info.filter(user=user)
        if librarian:
            return render(request, 'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')

    books = bookEntity_info.objects.all()
    book_form = forms.BookForm()
    return render(request, 'librarian/librarian_book.html',locals())

def librarian_CD(request):
    # 张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user = request.user
        librarian = librarian_info.filter(user=user)
        if librarian:
            return render(request, 'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')

    CDs = CD.objects.all()
    CDForm = forms.CDForm
    return render(request, 'librarian/librarian_CD.html',locals())

def bookshelf(request):
    # 张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user = request.user
        librarian = librarian_info.filter(user=user)
        if librarian:
            return render(request, 'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')
            
    bookShelfs = bookshelf_info.objects.all()
    BookShelfForm = forms.BookshelfForm()
    return render(request, 'librarian/bookshelf.html',locals())

def librarian_ebook(request):
    # 张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user = request.user
        librarian = librarian_info.filter(user=user)
        if librarian:
            return render(request, 'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')
            
    ebooks = ebook_info.objects.all()
    EbookForm = forms.EbookForm()
    return render(request, 'librarian/librarian_ebook.html', locals())

def librarian_usertype(request):
    # 张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user = request.user
        librarian = librarian_info.filter(user=user)
        if librarian:
            return render(request, 'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')
            
    userTypes = readerType.objects.all()
    userTypeForm = forms.ReaderTypeForm
    return render(request, 'librarian/librarian_usertype.html', locals())

def librarian_booktype(request):
    # 张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user = request.user
        librarian = librarian_info.filter(user=user)
        if librarian:
            return render(request, 'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')

    booktypes = booktype_info.objects.all()
    booktypeForm = forms.BookTypeForm
    return render(request, 'librarian/librarian_booktype.html',locals())

def librarian_borrow(request):
    # 张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user = request.user
        librarian = librarian_info.filter(user=user)
        if librarian:
            return render(request, 'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')
            
    borrows = Borrowing.objects.all()
    borrowForm = forms.BorrowingForm
    return render(request, 'librarian/librarian_borrow.html',locals())

def librarian_reser(request):
    # 张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user = request.user
        librarian = librarian_info.filter(user=user)
        if librarian:
            return render(request, 'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')
            
    resers = bookReser.objects.all()
    reserForm = forms.reserForm
    return render(request, 'librarian/librarian_reser.html',locals())

def librarian_user(request):
    # 张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user = request.user
        librarian = librarian_info.filter(user=user)
        if librarian:
            return render(request, 'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')
            
    readers =Reader.objects.all()
    ReaderForm = forms.ReaderForm()
    context = {
        'readers': readers,
        'ReaderForm':ReaderForm,
    }
    return render(request, 'librarian/librarian_user.html',context)

def add_user_to_database(request):
    # 张丽：加入馆员身份判断
    if request.session.get('is_login', None):
        return redirect('/')
    else:
        user = request.user
        librarian = librarian_info.filter(user=user)
        if librarian:
            return render(request, 'librarian/librarian.html')
        else:
            HttpResponse('馆员模块仅供本馆工作人员登录~')
            
    if request.method == "GET":
        userprofile_form = forms.AddReaderForm()
        return render(request, "librarian/userAddinfo.html",
                      locals())

    if request.method == "POST":
        new_user_form = forms.AddReaderForm(request.POST)
        if new_user_form.is_valid():
            username = new_user_form.cleaned_data['name']
            password = new_user_form.cleaned_data['Password']
            balance = new_user_form.cleaned_data['balance']
            max_borrowing = new_user_form.cleaned_data['max_borrowing']
            email = new_user_form.cleaned_data['email']
            Sex = new_user_form.cleaned_data['Sex']
            u = User.objects.get_or_create(username=email)[0]
            u.set_password(password)
            u.save()
            new_reader = Reader()
            new_reader.name = username
            new_reader.Password = password  # 使用加密密码
            new_reader.balance = balance
            new_reader.max_borrowing = max_borrowing
            new_reader.email = email
            new_reader.Sex = Sex
            new_reader.user = u
            new_reader.save()
            return redirect("../librarian/librarian_user")
        return redirect("../librarian/librarian_user")



def change_user_to_database(request):
    
    if request.method == "GET":
        id = request.GET["person_info_ptr_id"]
        reader = Reader.objects.get(person_info_ptr_id=id)
        initial = {"name": reader.name,
                   "Sex": reader.Sex,
                   #'email': reader.email,
                   'Password': reader.Password,
                   'balance': reader.balance,
                   'max_borrowing': reader.max_borrowing,
                   }
        userprofile_form = forms.ReaderForm(initial)
        return render(request, "librarian/userChangeinfo.html",
                      locals())

    if request.method == "POST":
        #a = request.POST.copy()
        #del a['email']
        change_user_form = forms.ReaderForm(request.POST)
        #change_user = Reader.objects.get(email = request.GET["email"])
        if change_user_form.is_valid():
            print("验证成功")
            #oldusername = change_user_form.cleaned_data['oldusername']
            username = change_user_form.cleaned_data['name']
            password = change_user_form.cleaned_data['Password']
            balance = change_user_form.cleaned_data['balance']
            max_borrowing = change_user_form.cleaned_data['max_borrowing']
            #email = change_user_form.cleaned_data['email']
            sex = change_user_form.cleaned_data['Sex']
            u = User.objects.get(username=request.GET["email"])
            print(u)
            print(Reader.objects.filter(email = request.GET["email"]))
            #change_user.update(user=u,name = username,Password = password,balance = balance,max_borrowing = max_borrowing,email = email,Sex = sex)
            Reader.objects.filter(email = request.GET["email"]).update(user=u,name = username,balance = balance,max_borrowing = max_borrowing,Password = password,Sex = sex)
            return redirect("../librarian/librarian_user")
        return redirect("../librarian/librarian_user")


def delete_user(request):
    Reader.objects.get(email = request.GET.get("email")).delete()
    User.objects.get(username=request.GET["email"]).delete()
    return redirect("librarian/librarian_user")

def delete_borrowing_to_database(request):
    Borrowing.objects.get(id = request.GET.get("id")).delete()
    return redirect("../librarian/librarian_borrow")
