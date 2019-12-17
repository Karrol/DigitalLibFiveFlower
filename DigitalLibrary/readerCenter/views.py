import datetime
from django.utils import timezone
from django.urls import reverse

from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from login.models import Reader, User
from search.models import book_info
from .forms import Change_reader_infoForm,UploadImageForm
from readerCenter.models import readerLibrary,readerSearchlist,Borrowing
from infoCenter.models import weekbook_info



# Create your views here.

# 个人中心页面-个人资料
def profile(request):
    if not request.user.is_authenticated:
        return redirect("login:readerLogin")

    id = request.user.id
    try:
        reader = Reader.objects.get(user_id=id)
    except Reader.DoesNotExist:
        return HttpResponse('no this id reader')

    # 判断用户状态，如果是登录用户，记录其现在浏览的位置，游客则不记录
    if request.user.is_authenticated:
        request.session['user_location'] = 'readerCenter:profile'

    borrowing = Borrowing.objects.filter(reader=reader).exclude(date_returned__isnull=False)

    context = {
        'state': request.GET.get('state', None),
        'reader': reader,
    }
    return render(request, 'readerCenter/profile.html', context)


# 读者修改个人信息表单
@login_required
def readerChangeinfo(request):
    '''把已有的用户信息读出来，然后判断用户请求是POST还是GET。如果是GET，则显示表单,并将用户已有信息也显示在其中，如果是POST，则接收用户提交的表单信息，然后更新各个数据模型实例属性的值'''
    user = User.objects.get(username=request.user.username)
    userprofile = Reader.objects.get(user=request.user)

    if request.method == "POST":
        userprofile_form = Change_reader_infoForm(request.POST)
        message='请注意检查填写内容'
        if userprofile_form.is_valid():
            user_cd = userprofile_form.cleaned_data
            userprofile.name = user_cd['name']
            userprofile.sex = user_cd['sex']
            userprofile.save()
            message='success'
        context={
             'userprofile_form':userprofile_form,
             'message':message,
        }
        return render(request, 'readerCenter/readerChangeinfo.html', context)
    else:
        userprofile_form = Change_reader_infoForm(initial={"name": userprofile.name, "sex": userprofile.Sex})
        return render(request, "readerCenter/readerChangeinfo.html",
                      locals())
    

 #上传图片
@login_required
def uploadImg(request):
    if request.method == 'GET':
        uploadImgForm = UploadImageForm(request.POST, request.FILES)
        return render(request, 'readerCenter/readerUploadPhoto.html',locals())
        # 添加头像图片，接收到img的url
    email=request.session['user_email']
    reader=Reader.objects.get(email=email)
    uploadImgForm = UploadImageForm(request.POST, request.FILES)
    message='fail'
    if request.method == 'POST':
        img = request.FILES.get('photo')
        reader.photo=img
        reader.save()
        message='success'
        return render(request, 'readerCenter/readerUploadPhoto.html',locals())
    return render(request, 'readerCenter/readerUploadPhoto.html',locals())


# 个人中心-读者通知界面
@login_required
def readerNotice(request):
    # 判断用户状态，如果是登录用户，记录其现在浏览的位置
    if request.user.is_authenticated:
        request.session['user_location'] = 'readerCenter:readerNotice'
    reader = Reader.objects.get(user=request.user)
    # 每周一书的通知-仅推荐当周推荐，点击更多可以查看历史推荐
    book_week = weekbook_info.objects.filter(now_display=True)

    #实现系统自动进行借阅催还功能
    book_over=Borrowing.objects.filter(reader=reader)

    return render(request, 'readerCenter/readerNotice.html', locals())



# 个人中心-读者通知阅读界面  
@login_required
def showNotice(request):
    articleID = request.GET.get('aticleID', None)
    print(articleID)
    if not articleID:
        return HttpResponse('there is no such an aticleID')
    try:
        notice = article_info.objects.get(pk=articleID)
    except notice.DoesNotExist:
        return HttpResponse('there is no such an articleID')
    state = None
    # 如果是每周一书，则要显示书籍的信息
    # 为什么永远都不是每周一书
    if notice.articleID.startswith('week'):
        # 获取书籍的信息
        wbook = weekbook.objects.get(articleID=articleID)
        wbook_info = book_info.objects.get(pk=wbook.ISBN.ISBN)
        state = 'weekbook_notice'
        # wbook.ISBN=wbook_info
        # wbook.save()
        context = {
            'wbook_info': wbook_info,
            'notice': notice,
            'state': state,
        }
        return render(request, 'readerCenter/noticeDetail.html', context)
    else:
        state = 'normal_notice'
        context = {'notice': notice,
                   'state': state, }
        return render(request, 'readerCenter/noticeDetail.html', context)


# 查询借阅状态页面
@login_required
def readerBorrowing(request):
    # 判断用户状态，如果是登录用户，记录其现在浏览的位置
    if request.user.is_authenticated:
        request.session['user_location'] = 'readerCenter:readerBorrowing'
        
    id = request.user.id
    try:
        reader = Reader.objects.get(user_id=id)
    except Reader.DoesNotExist:
        return HttpResponse('no this id reader')

    borrowing = Borrowing.objects.filter(reader=reader).exclude(date_returned__isnull=False)

    context = {
        'state': request.GET.get('state', None),
        'reader': reader,
        'borrowing': borrowing,
    }
    return render(request, 'readerCenter/readerBorSituation.html', context)

#读者在我的借阅的的借还操作
@login_required
def readerOperateBook(request):
    action = request.GET.get('action', None)
    if action == 'return_book':
        id = request.GET.get('id', None)
        if not id:
            return HttpResponse('no id')
        b = Borrowing.objects.get(pk=id)
        b.date_returned = datetime.date.today()
        if b.date_returned > b.date_due_to_returned:
            b.amount_of_fine = (b.date_returned - b.date_due_to_returned).total_seconds() / 24 / 3600 * 0.1
        b.save()

        r = Reader.objects.get(user=request.user)
        r.max_borrowing += 1
        r.save()

        bk = book_info.objects.get(ISBN=b.ISBN_id)
        bk.quantity += 1
        bk.save()

        return HttpResponseRedirect('/bowrrowing?state=return_success')
    elif action == 'renew_book':
        id = request.GET.get('id', None)
        if not id:
            return HttpResponse('no id')
        b = Borrowing.objects.get(pk=id)
        if (b.date_due_to_returned - b.date_issued) < datetime.timedelta(60):
            b.date_due_to_returned += datetime.timedelta(30)
            b.save()

        return HttpResponseRedirect('/bowrrowing?state=renew_success')

    return HttpResponseRedirect('/bowrrowing')

# 从检索首页的导航栏入口/个人中心入口进入查询结果页
@login_required
def show_mysearchlist(request):
    # 判断用户状态，如果是登录用户，记录其现在浏览的位置
    if request.user.is_authenticated:
        request.session['user_location'] = 'readerCenter:searchlist'
    searchlists = []
    # 获取当前页面的url
    current_path = request.get_full_path()
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login:readerLogin')
    else:
        # 获取传递过来读者ID
        reader = Reader.objects.get(user_id=request.user.id)
        searchlists = readerSearchlist.objects.filter(reader=reader).order_by('-search_date')[0:50]

        # 翻页功能实现
        paginator = Paginator(searchlists, 5)
        page = request.GET.get('page', 1)

        try:
            searchlists = paginator.page(page)
        except PageNotAnInteger:
            searchlists = paginator.page(1)
        except EmptyPage:
            searchlists = paginator.page(paginator.num_pages)

        # ugly solution for &page=2&page=3&page=4
        if '&page' in current_path:
            current_path = current_path.split('&page')[0]

        context = {
            'current_path': current_path,

            "searchlists": searchlists,

        }
        return render(request, 'readerCenter/searchlist.html', context)


# 将搜索结果添加至“查询结果”页面
@login_required
# @permission_required('Information.delete_information', raise_exception=True)
def add_to_searchlist(request):
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login:readerLogin')
    else:
        # 获取传递过来的ISBN号以及读者ID
        variables = request.GET['ISBN']
        reader = Reader.objects.get(user_id=request.user.id)
        # 实现数据库添加操作，实现“查询界面”的数据传递到“查询结果”页面
        for item in variables.split(','):  # 拆分多个ISBN号连结而成的字符串，形成ISBN号列表
            # 定义一个临时的书籍对象来存储数据信息
            bk = book_info.objects.get(ISBN=item)
            # bk.quantity -= 1   #电子书不需要库存减一
            bk.save()
            date = timezone.now()
            # 在表“mysearchlist”中创建记录存bk对象的数据
            searchlist = readerSearchlist.objects.create(
                reader=reader,
                ISBN=bk,  # 注意：这样赋值后，书的ISBN是个BOOK实例！？以致于在template代码中有book_info.ISBN.ISBN的变量出现
                search_date=date)
            searchlist.save()
        state = 'success'  # 数据库存取操作完成
        if (state == 'success'):
            searchlists = readerSearchlist.objects.filter(reader=reader)
            context = {"searchlists": searchlists}
            return render(request, 'readerCenter/searchlist.html', context)

    return redirect(reverse('readerCenter:searchlist'))


# 删除“查询结果”页面中的书籍
@login_required
# @permission_required('Information.delete_information', raise_exception=True)
def delete_from_searchlist(request):
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login:readerLogin')
    else:
        # 获取传递过来的查询记录的id以及读者ID
        variables = request.GET['id']
        reader = Reader.objects.get(user_id=request.user.id)
        # 实现数据库添加操作，实现“查询界面”的数据传递到“查询结果”页面
        for item in variables.split(','):  # 拆分多个查询记录id连结而成的字符串，形成id列表
            bk = get_object_or_404(readerSearchlist, pk=int(item))
            bk.delete()
        state = 'success'  # 数据库删除操作完成
        if (state == 'success'):
            searchlists = readerSearchlist.objects.filter(reader=reader)
            context = {"searchlists": searchlists}
            return render(request, 'readerCenter/searchlist.html', context)

    return HttpResponseRedirect(reverse('readerCenter:searchlist'))





# 显示“我的图书馆”页面，添加图书到我的图书馆页面的代码见“library:def book_detail”
# "readerCenter:def mylib"应该完成显示我的图书馆书籍
@login_required
def mylib(request):
    # 判断用户状态，如果是登录用户，记录其现在浏览的位置
    if request.user.is_authenticated:
        request.session['user_location'] = 'readerCenter:mylib'

    id = request.user.id
    try:
        reader = Reader.objects.get(user_id=id)
    except Reader.DoesNotExist:
        return HttpResponse('no this id reader')
    mylib_list = readerLibrary.objects.filter(reader=reader)

    context = {
        'state': request.GET.get('state', None),
        'reader': reader,
        'mylib_list': mylib_list,
    }
    return render(request, 'readerCenter/mylib.html', context)

# “我的图书馆”界面内书籍的管理操作：增+删+查
@login_required
#我的图书馆删除功能
def mylib_del(request,ISBN):
    isbn =ISBN
    id = request.user.id
    reader = Reader.objects.get(user_id=id)
    state = None
    mylib_list = readerLibrary.objects.filter(reader=reader,ISBN=isbn)
    book = readerLibrary.objects.get(reader=reader, ISBN=isbn)
    if book:
        book.delete()
        state = 'delete_from_mylib_success'
    else:
        state = 'delete_from_mylib_fail'
    context = {
        'state': state,
        'reader': reader,
        'mylib_list': mylib_list,
    }
    return render(request, 'readerCenter/mylib.html', context)


#我的图书馆添加图书功能
def mylib_add(request,ISBN):
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return redirect('login:readerLogin')
    else:
        # 获取传递过来的查询记录的id以及读者ID
        id = request.user.id
        reader = Reader.objects.get(user_id=request.user.id)
    isbn = ISBN
    state = None
    message = None
    repeat_book = readerLibrary.objects.filter(reader=reader,ISBN=isbn)
    book=book_info.objects.filter(ISBN=isbn)
    mylib_list=readerLibrary.objects.filter(reader=reader)
    if not book:
        state='book_not_exist'
    elif repeat_book:
        state = 'repeat_add'
    else:
        nowdate = datetime.date.today()
        bk = book_info.objects.get(ISBN=isbn)
        mylib_new_book = readerLibrary.objects.create(reader=reader, ISBN=bk, In_date=nowdate)
        mylib_new_book.save()
        state = 'add_to_mylib_success'
        
    user_location=request.session.get('user_location')

    if user_location=='search:searchBook':
        message='back_to_search_searchBook'

    context = {
        'state': state,
        'reader': reader,
        'mylib_list': mylib_list,
        'message':message,
    }
    return render(request, 'readerCenter/mylib.html', context)


@login_required
# 我的图书馆查找图书功能
def mylib_search(request):
    id = request.user.id
    reader = Reader.objects.get(user_id=id)
    keyword=request.GET.get['MylibSearchKeyword']
    
    mylib_books = readerLibrary.objects.filter(reader=reader)
    searchResultISBN=[]
    counter=0
    for book in mylib_books:
        if book.ISBN.title==keyword:
            searchResultISBN[counter]=book.ISBN
            counter=counter+1
        elif book.ISBN.author==keyword:
            searchResultISBN[counter] = book.ISBN
            counter = counter + 1
        elif book.ISBN.ISBN==keyword:
            searchResultISBN[counter] = book.ISBN
            counter = counter + 1
        elif book.ISBN.category==keyword:
            searchResultISBN[counter] = book.ISBN
            counter = counter + 1

    context={'searchResultISBN':searchResultISBN,}
    return render(request, 'readerCenter/mylib.html',context)



# 2019-11-提供删除我的图书馆内书籍的功能-未开发完毕，还需学习借书、还书实现的过程
def delete_from_mylib(request):
    isbn = request.GET.get('ISBN', None)
    print(isbn)
    '''if not ISBN:
        return HttpResponse('there is no such an ISBN')
    try:
        book = book_info.objects.get(pk=ISBN)
    except book_info.DoesNotExist:
        return HttpResponse('there is no such an ISBN')'''

    action = request.GET.get('action', None)
    state = None

    # 获取用户信息
    id = request.user.id
    reader = Reader.objects.get(user_id=id)
    if action == 'delete_from_mylib':
        book = readerLibrary.objects.get(reader=reader, ISBN=isbn)
        book.delete()
        book.save()
        state = 'delete_from_mylib_success'
        return HttpResponseRedirect('/mylib?state=delete_from_mylib_success')
    else:
        state = 'delete_from_mylib_fail'
        return HttpResponseRedirect('/mylib?state=delete_from_mylib_fail')


# 将搜索结果添加至“查询结果”页面
@login_required
# @permission_required('Information.delete_information', raise_exception=True)
def add_to_searchlist(request):
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login:readerLogin')
    else:
        # 获取传递过来的ISBN号以及读者ID
        variables = request.GET['ISBN']
        reader = Reader.objects.get(user_id=request.user.id)
        # 实现数据库添加操作，实现“查询界面”的数据传递到“查询结果”页面
        for item in variables.split(','):  # 拆分多个ISBN号连结而成的字符串，形成ISBN号列表
            # 定义一个临时的书籍对象来存储数据信息
            bk = book_info.objects.get(ISBN=item)
            # bk.quantity -= 1   #电子书不需要库存减一
            bk.save()
            date = timezone.now()
            # 在表“mysearchlist”中创建记录存bk对象的数据
            searchlist = readerSearchlist.objects.create(
                reader=reader,
                ISBN=bk,  # 注意：这样赋值后，书的ISBN是个BOOK实例！？以致于在template代码中有book_info.ISBN.ISBN的变量出现
                search_date=date)
            searchlist.save()
        state = 'success'  # 数据库存取操作完成
        if (state == 'success'):
            searchlists = readerSearchlist.objects.filter(reader=reader)
            context = {"searchlists": searchlists}
            return render(request, 'readerCenter/searchlist.html', context)

    return HttpResponseRedirect(reverse('readerCenter:searchlist'))


# 删除“查询结果”页面中的书籍
@login_required
# @permission_required('Information.delete_information', raise_exception=True)
def delete_from_searchlist(request):
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login:readerLogin')
    else:
        # 获取传递过来的查询记录的id以及读者ID
        variables = request.GET['id']
        reader = Reader.objects.get(user_id=request.user.id)
        # 实现数据库添加操作，实现“查询界面”的数据传递到“查询结果”页面
        for item in variables.split(','):  # 拆分多个查询记录id连结而成的字符串，形成id列表
            bk = get_object_or_404(readerSearchlist, pk=int(item))
            bk.delete()
        state = 'success'  # 数据库删除操作完成
        if (state == 'success'):
            searchlists = readerSearchlist.objects.filter(reader=reader)
            context = {"searchlists": searchlists}
            return render(request, 'readerCenter/searchlist.html', context)

    return HttpResponseRedirect(reverse('readerCenter:searchlist'))
