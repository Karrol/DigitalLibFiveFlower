from django.shortcuts import render,redirect
from django.http import  HttpResponse
#from librarian.models import bookborrow_info,bookback_info, reader_info
from login.models import Reader, readerType, librarian_info
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
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user=request.user
        librarian=librarian_info.objects.filter(user=user)
        if librarian:
            return render(request,'librarian/librarian.html')
        else:
            return HttpResponse('馆员模块仅供本馆工作人员登录~')


def librarian_book(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user=request.user
        librarian=librarian_info.objects.filter(user=user)
        if librarian:
            books = bookEntity_info.objects.all()
            book_form = forms.BookForm()
            return render(request, 'librarian/librarian_book.html',locals())
        else:
            return HttpResponse('馆员模块仅供本馆工作人员登录~')


def librarian_CD(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user=request.user
        librarian=librarian_info.objects.filter(user=user)
        if librarian:
            CDs = CD.objects.all()
            CDForm = forms.CDForm
            return render(request, 'librarian/librarian_CD.html',locals())
        else:
            return HttpResponse('馆员模块仅供本馆工作人员登录~')


def bookshelf(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user=request.user
        librarian=librarian_info.objects.filter(user=user)
        if librarian:
            bookShelfs = bookshelf_info.objects.all()
            BookShelfForm = forms.BookshelfForm()
            return render(request, 'librarian/bookshelf.html',locals())
        else:
            return HttpResponse('馆员模块仅供本馆工作人员登录~')



def librarian_ebook(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user=request.user
        librarian=librarian_info.objects.filter(user=user)
        if librarian:
            ebooks = ebook_info.objects.all()
            EbookForm = forms.EbookForm()
            return render(request, 'librarian/librarian_ebook.html', locals())
        else:
            return HttpResponse('馆员模块仅供本馆工作人员登录~')


def librarian_usertype(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user=request.user
        librarian=librarian_info.objects.filter(user=user)
        if librarian:
            userTypes = readerType.objects.all()
            userTypeForm = forms.ReaderTypeForm
            return render(request, 'librarian/librarian_usertype.html', locals())
        else:
            return HttpResponse('馆员模块仅供本馆工作人员登录~')


def librarian_booktype(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user=request.user
        librarian=librarian_info.objects.filter(user=user)
        if librarian:
            booktypes = booktype_info.objects.all()
            booktypeForm = forms.BookTypeForm
            return render(request, 'librarian/librarian_booktype.html',locals())
        else:
            return HttpResponse('馆员模块仅供本馆工作人员登录~')


def librarian_borrow(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user=request.user
        librarian=librarian_info.objects.filter(user=user)
        if librarian:
            borrows = Borrowing.objects.all()
            borrowForm = forms.BorrowingForm
            return render(request, 'librarian/librarian_borrow.html',locals())
        else:
            return HttpResponse('馆员模块仅供本馆工作人员登录~')


def librarian_reser(request):
    if not request.user.is_authenticated:
        return redirect('/')
    else:
        user=request.user
        librarian=librarian_info.objects.filter(user=user)
        if librarian:
            resers = bookReser.objects.all()
            reserForm = forms.reserForm
            return render(request, 'librarian/librarian_reser.html',locals())
        else:
            return HttpResponse('馆员模块仅供本馆工作人员登录~')


def librarian_user(request):
    
        user=request.user
        librarian=librarian_info.objects.filter(user=user)
        if librarian:
            readers =Reader.objects.all()
            ReaderForm = forms.ReaderForm()
            context = {
                    'readers': readers,
                    'ReaderForm':ReaderForm,
                    }
            return render(request, 'librarian/librarian_user.html',context)
        else:
            return HttpResponse('馆员模块仅供本馆工作人员登录~')


def add_user_to_database(request):
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

def add_book_to_database(request):
    if request.method == "GET":
        userprofile_form = forms.BookForm()
        return render(request, "librarian/BookAddinfo.html",
                      locals())

    if request.method == "POST":
        new_book_form = forms.BookForm(request.POST)
        id_list = bookEntity_info.objects.values("id")
        max = 0
        for id in id_list:
            if max <= id['id']:
                max = id['id']
        id = max+1
        print(id)
        if new_book_form.is_valid():
            location = new_book_form.cleaned_data['location']
            quantity = new_book_form.cleaned_data['quantity']
            booksearchID = new_book_form.cleaned_data['booksearchID']
            bookIntime = new_book_form.cleaned_data['bookIntime']
            bookshelfid  = new_book_form.cleaned_data['bookshelfid']
            new_book = bookEntity_info()
            new_book.id = id
            new_book.location = location
            new_book.quantity = quantity # 使用加密密码
            new_book.booksearchID = booksearchID
            new_book.bookIntime = bookIntime
            new_book.bookshelfid  = bookshelfid
            new_book.save()
            return redirect("../librarian/librarian_book")
        return redirect("../librarian/librarian_book")

def add_CD_to_database(request):
    if request.method == "GET":
        userprofile_form = forms.CDForm()
        action = add_CD_to_database
        tishi = "增加光碟信息"
        return render(request, "librarian/Addinfo.html",
                      locals())

    if request.method == "POST":
        new_book_form = forms.CDForm(request.POST)
        id_list = CD.objects.values("id")
        max = 0
        for id in id_list:
            if max <= id['id']:
                max = id['id']
        id = max+1
        print(id)
        if new_book_form.is_valid():
            title = new_book_form.cleaned_data['title']
            author = new_book_form.cleaned_data['author']
            cdId = new_book_form.cleaned_data['cdId']
            new_CD = CD()
            new_CD.id = id
            new_CD.title = title
            new_CD.author = author # 使用加密密码
            new_CD.cdId = cdId
            new_CD.save()
            return redirect("../librarian/librarian_CD")
        return redirect("../librarian/librarian_CD")

def add_usertype_to_database(request):
    if request.method == "GET":
        userprofile_form = forms.ReaderTypeForm()
        action = add_usertype_to_database
        tishi = "增加读者类型信息"
        return render(request, "librarian/Addinfo.html",
                      locals())

    if request.method == "POST":
        new_book_form = forms.ReaderTypeForm(request.POST)
        id_list = readerType.objects.values("id")
        max = 0
        for id in id_list:
            if max <= id['id']:
                max = id['id']
        id = max+1
        print(id)
        if new_book_form.is_valid():
            typeName = new_book_form.cleaned_data['typeName']
            bookNum = new_book_form.cleaned_data['bookNum']
            new_usertype = readerType()
            new_usertype.id = id
            new_usertype.typeName = typeName
            new_usertype.bookNum = bookNum #
            new_usertype.save()
            return redirect("../librarian/librarian_Usertype")
        return redirect("../librarian/librarian_Usertype")

def add_booktype_to_database(request):
    if request.method == "GET":
        userprofile_form = forms.BookTypeForm()
        action = add_booktype_to_database
        tishi = "增加图书类型信息"
        return render(request, "librarian/Addinfo.html",locals())

    if request.method == "POST":
        new_book_form = forms.BookTypeForm(request.POST)
        id_list = booktype_info.objects.values("btID")
        max = 0
        for id in id_list:
            if max <= id['btID']:
                max = id['btID']
        id = max+1
        print(id)
        if new_book_form.is_valid():
            btName = new_book_form.cleaned_data['btName']
            bookType = new_book_form.cleaned_data['bookType']
            booktype = booktype_info()
            booktype.btID = id
            booktype.btName = btName
            booktype.bookType = bookType
            booktype.save()
            return redirect("../librarian/librarian_Booktype")
        return redirect("../librarian/librarian_Booktype")

def add_bookshelf_to_database(request):
    if request.method == "GET":
        userprofile_form = forms.BookshelfForm()
        action = add_bookshelf_to_database
        tishi = "增加书架信息"
        return render(request, "librarian/Addinfo.html",locals())

    if request.method == "POST":
        new_book_form = forms.BookshelfForm(request.POST)
        id_list = bookshelf_info.objects.values("bookshelfID")
        max = 0
        for id in id_list:
            if max <= int(id['bookshelfID'][3:]):
                max = int(id['bookshelfID'][3:])
        id = 'bks{}'.format(max+1)
        print(id)
        if new_book_form.is_valid():
            bookshelfName = new_book_form.cleaned_data['bookshelfName']
            bookshelf = bookshelf_info()
            bookshelf.bookshelfID = id
            bookshelf.bookshelfName = bookshelfName
            bookshelf.save()
            return redirect("../librarian/bookshelf")
        return redirect("../librarian/bookshelf")

def add_ebook_to_database(request):
    if request.method == "GET":
        userprofile_form = forms.EbookForm()
        action = add_ebook_to_database
        tishi = "增加电子图书信息"
        return render(request, "librarian/Addinfo.html",locals())

    if request.method == "POST":
        new_book_form = forms.EbookForm(request.POST)
        id_list = ebook_info.objects.values("ebookID")
        max = 0
        for id in id_list:
            if max <= id['ebookID']:
                max = id['ebookID']
        id = max+1
        print(id)
        if new_book_form.is_valid():
            ebookName = new_book_form.cleaned_data['ebookName']
            ebookAuthor = new_book_form.cleaned_data['ebookAuthor']
            ebookTranslator = new_book_form.cleaned_data['ebookTranslator']
            ebookPress = new_book_form.cleaned_data['ebookPress']
            ebookIntime = new_book_form.cleaned_data['ebookIntime']
            ebookResource = new_book_form.cleaned_data['ebookResource']
            ebookPage = new_book_form.cleaned_data['ebookPage']
            ebook = ebook_info()
            ebook.ebookName = ebookName
            ebook.ebookAuthor = ebookAuthor
            ebook.ebookTranslator = ebookTranslator
            ebook.ebookPress = ebookPress
            ebook.ebookIntime = ebookIntime
            ebook.ebookResource = ebookResource
            ebook.ebookPage = ebookPage
            ebook.save()
            return redirect("../librarian/librarian_ebook")
        return redirect("../librarian/librarian_ebook")


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

def change_book_to_database(request):
    if request.method == "GET":
        id = request.GET["id"]
        book =bookEntity_info.objects.get(id=id)
        initial = {
            "location" : book.location,
            "quantity" : book.quantity,
            "booksearchID" : book.booksearchID,
            "bookIntime" : book.bookIntime,
            "bookshelfid" : book.bookshelfid
                   }
        userprofile_form = forms.BookForm(initial)
        return render(request, "librarian/BookChangeinfo.html",
                      locals())

    if request.method == "POST":
        change_book_form = forms.BookForm(request.POST)
        #change_user = Reader.objects.get(email = request.GET["email"])
        if change_book_form.is_valid():
            location = change_book_form.cleaned_data['location']
            quantity = change_book_form.cleaned_data['quantity']
            booksearchID = change_book_form.cleaned_data['booksearchID']
            bookIntime = change_book_form.cleaned_data['bookIntime']
            bookshelfid  = change_book_form.cleaned_data['bookshelfid']
            bookEntity_info.objects.filter(id = request.GET["id"]).update(location=location,quantity = quantity,booksearchID = booksearchID,bookIntime = bookIntime,bookshelfid = bookshelfid)
            return redirect("../librarian/librarian_book")
        return redirect("../librarian/librarian_book")

def change_CD_to_database(request):
    if request.method == "GET":
        id = request.GET["id"]
        cd = CD.objects.get(id=id)
        initial = {
            "title" : cd.title,
            "author" : cd.author,
            "cdId" : cd.cdId,
                   }
        userprofile_form = forms.CDForm(initial)
        return render(request, "librarian/CDChangeinfo.html",
                      locals())

    if request.method == "POST":
        change_book_form = forms.CDForm(request.POST)
        #change_user = Reader.objects.get(email = request.GET["email"])
        if change_book_form.is_valid():
            title = change_book_form.cleaned_data['title']
            author = change_book_form.cleaned_data['author']
            cdId = change_book_form.cleaned_data['cdId']
            CD.objects.filter(id = request.GET["id"]).update(title = title,author = author,cdId = cdId)
            return redirect("../librarian/librarian_CD")
        return redirect("../librarian/librarian_CD")

def change_usertype_to_database(request):
    if request.method == "GET":
        id = request.GET["id"]
        usertype = readerType.objects.get(id=id)
        initial = {
            "typeName" : usertype.typeName,
            "bookNum" : usertype.bookNum,
                   }
        userprofile_form = forms.ReaderTypeForm(initial)
        return render(request, "librarian/usertypeChangeinfo.html",
                      locals())

    if request.method == "POST":
        change_book_form = forms.ReaderTypeForm(request.POST)
        #change_user = Reader.objects.get(email = request.GET["email"])
        if change_book_form.is_valid():
            typeName = change_book_form.cleaned_data['typeName']
            bookNum = change_book_form.cleaned_data['bookNum']
            readerType.objects.filter(id = request.GET["id"]).update(typeName = typeName,bookNum = bookNum)
            return redirect("../librarian/librarian_Usertype")
        return redirect("../librarian/librarian_Usertype")

def change_booktype_to_database(request):
    if request.method == "GET":
        id = request.GET["btID"]
        booktype = booktype_info.objects.get(btID=id)
        initial = {
            "btName" : booktype.tbName,
            "bookType" : booktype.bookType,
                   }
        userprofile_form = forms.BookTypeForm(initial)
        return render(request, "librarian/booktypeChangeinfo.html",
                      locals())

    if request.method == "POST":
        change_book_form = forms.BookTypeForm(request.POST)
        #change_user = Reader.objects.get(email = request.GET["email"])
        if change_book_form.is_valid():
            btName = change_book_form.cleaned_data['btName']
            bookType = change_book_form.cleaned_data['bookTYpe']
            readerType.objects.filter(btID = request.GET["id"]).update(btName = btName,bookTYpe = bookType)
            return redirect("../librarian/librarian_Booktype")
        return redirect("../librarian/librarian_Booktype")

def change_bookshelf_to_database(request):
    if request.method == "GET":
        id = request.GET["bookshelfID"]
        bookshelf = bookshelf_info.objects.get(bookshelfID=id)
        initial = {
            "bookshelfName" : bookshelf.bookshelfName,
                   }
        userprofile_form = forms.BookshelfForm(initial)
        return render(request, "librarian/bookshelfChangeinfo.html",
                      locals())

    if request.method == "POST":
        change_book_form = forms.BookshelfForm(request.POST)
        #change_user = Reader.objects.get(email = request.GET["email"])
        if change_book_form.is_valid():
            bookshelfName = change_book_form.cleaned_data['bookshelfName']
            bookshelf_info.objects.filter(bookshelfID = request.GET["bookshelfID"]).update(bookshelfName=bookshelfName)
            return redirect("../librarian/bookshelf")
        return redirect("../librarian/bookshelf")

def change_ebook_to_database(request):
    if request.method == "GET":
        id = request.GET["ebookID"]
        ebook = ebook_info.objects.get(ebookID=id)
        initial = {
            "ebookName":ebook.ebookName,
            "ebookAuthor":ebook.ebookAuthor,
            "ebookTranslator":ebook.ebookTranslator,
            "ebookPress":ebook.ebookPress,
            "ebookIntime":ebook.ebookIntime,
            "ebookResource":ebook.ebookResource
                   }
        userprofile_form = forms.EbookForm(initial)
        return render(request, "librarian/bookshelfChangeinfo.html",
                      locals())

    if request.method == "POST":
        new_book_form = forms.EbookForm(request.POST)
        id_list = ebook_info.objects.values("ebookID")
        max = 0
        for id in id_list:
            if max <= id['ebookID']:
                max = id['ebookID']
        id = max+1
        print(id)
        if new_book_form.is_valid():
            ebookName = new_book_form.cleaned_data['ebookName']
            ebookAuthor = new_book_form.cleaned_data['ebookAuthor']
            ebookTranslator = new_book_form.cleaned_data['ebookTranslator']
            ebookPress = new_book_form.cleaned_data['ebookPress']
            ebookIntime = new_book_form.cleaned_data['ebookIntime']
            ebookResource = new_book_form.cleaned_data['ebookResource']
            ebook = ebook_info()
            ebook.ebookName = ebookName
            ebook.ebookAuthor = ebookAuthor
            ebook.ebookTranslator = ebookTranslator
            ebook.ebookPress = ebookPress
            ebook.ebookIntime = ebookIntime
            ebook.ebookResource = ebookResource
            ebook.save()
            return redirect("../librarian/librarian_ebook")
        change_book_form = forms.EbookForm(request.POST)
        #change_user = Reader.objects.get(email = request.GET["email"])
        if change_book_form.is_valid():
            ebookName = change_book_form.cleaned_data['ebookName']
            ebookAuthor = change_book_form.cleaned_data['ebookAuthor']
            ebookTranslator = change_book_form.cleaned_data['ebookTranslator']
            ebookPress = change_book_form.cleaned_data['ebookPress']
            ebookIntime = change_book_form.cleaned_data['ebookIntime']
            ebookResource = change_book_form.cleaned_data['ebookResource']
            ebook_info.objects.filter(ebookID = request.GET["ebookID"]).update(ebookName = ebookName,ebookAuthor = ebookAuthor,ebookTranslator = ebookTranslator,ebookPress = ebookPress,ebookIntime = ebookIntime,ebookResource = ebookResource)
            return redirect("../librarian/librarian_ebook")
        return redirect("../librarian/librarian_ebook")

def delete_user(request):
    Reader.objects.get(email = request.GET.get("email")).delete()
    User.objects.get(username=request.GET["email"]).delete()
    return redirect("../librarian/librarian_user")

def delete_borrowing_to_database(request):
    Borrowing.objects.get(id = request.GET.get("id")).delete()
    return redirect("../librarian/librarian_borrow")

def delete_book_to_database(request):
    bookEntity_info.objects.get(id = request.GET.get("id")).delete()
    return redirect("../librarian/librarian_book")

def delete_usertype_to_database(request):
    readerType.objects.get(id = request.GET.get("id")).delete()
    return redirect("../librarian/librarian_Usertype")

def delete_booktype_to_database(request):
    booktype_info.objects.get(btID = request.GET.get("btID")).delete()
    return redirect("../librarian/librarian_Booktype")

def delete_ebook_to_database(request):
    ebook_info.objects.get(ebookID = request.GET.get("ebookID")).delete()
    return redirect("../librarian/librarian_ebook")

def delete_bookshelf_to_database(request):
    bookshelf_info.objects.get(bookshelfID = request.GET.get("bookshelfID")).delete()
    return redirect("../librarian/bookshelf")

def delete_CD_to_database(request):
    CD.objects.get(id = request.GET.get("id")).delete()
    return redirect("../librarian/librarian_CD")
