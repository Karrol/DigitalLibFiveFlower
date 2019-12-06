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
from .forms import Change_reader_infoForm
from readerCenter.models import readerLibrary,readerSearchlist,Borrowing
from infoCenter.models import weekbook_info



# Create your views here.

# 个人中心页面-个人资料
def profile(request):
    if not request.user.is_authenticated:
        return redirect("login:user_login")

    id = request.user.id
    try:
        reader = Reader.objects.get(user_id=id)
    except Reader.DoesNotExist:
        return HttpResponse('no this id reader')

    borrowing = Borrowing.objects.filter(reader=reader).exclude(date_returned__isnull=False)

    context = {
        'state': request.GET.get('state', None),
        'reader': reader,
    }
    return render(request, 'readerCenter/profile.html', context)


# 读者修改个人信息表单
@login_required
def readerChangeinfo(request):
    reader = Reader.objects.get(user=request.user)
    state = None
    if request.method == 'POST':
        reader.name = request.POST.get('name', '')
        # photo的上传有问题，还有就是要给读者原始信息的提示
        reader.photo = request.POST.get('photo', '')
        reader.email = request.POST.get('email', '')
        reader.save()
        state = 'success'
    context = {
        'Change_reader_infoForm': Change_reader_infoForm(),
        'state': state,
    }

    return render(request, 'readerCenter/readerChangeinfo.html', context)


# 个人中心-读者通知界面
@login_required
def readerNotice(request):
    reader = Reader.objects.get(user=request.user)
    # 每周一书的通知-仅推荐当周推荐，点击更多可以查看历史推荐
    book_week = weekbook_info.objects.get(now_display=True)

    #实现系统自动进行借阅催还功能
    state_to_return = None
    state_over = None
    # 设变量用来存储应还书、超期书的书名
    book_to_return = ''
    book_over_time = ''
    #判断用户是否有在借图书
    lending_book=Borrowing.objects.filter(reader=reader)
    #遍历用户在借书籍
    for book in lending_book:
        #获取该图书应还日期
        lendBookTime=book.date_due_to_returned
        #判断是否超出还书时间
        today=datetime.date.today()
        #判断此书是否已还
        if book.date_returned:
            continue
        else:
            if today>lendBookTime:
                #超时，生成催还提醒标题
                state_over='book_over_time'
                #获得超时书籍列表
                book_over_time=book_over_time+','+book.ISBN.title
            else:
                # 没有超时，判断距离还书日期是否小于等于3天
                if (lendBookTime-today)<=3:
                    # 小于等于，返回催还通知
                    state_to_return='its_time_to_return'
                    book_to_return=book_to_return+','+book.ISBN.title
                else:
                    #大于，不显示催还通知,用户在借书籍情况的state=none
                    state_to_return = None
                    state_over = None
                
    nowtime = timezone.now()

    context = {
        "reader": reader,
        "state_to_return": state_to_return,
        "state_over": state_over,
        "book_week": book_week,
        "nowtime": nowtime,
        "book_over_time": book_over_time,
        "book_to_return": book_to_return,

    }
    return render(request, 'readerCenter/readerNotice.html', context)



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
def readerBorrowing(request):
    if not request.user.is_authenticated:
        return redirect('login:login')

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
def readerOperateBook(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

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

# 从检索首页的导航栏入口进入查询结果页
@login_required
def show_mysearchlist(request):
    searchlists = []
    # 获取当前页面的url
    current_path = request.get_full_path()
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('library:login')
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
        return HttpResponseRedirect('/login')
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
        return HttpResponseRedirect('/login')
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


# 从个人中心导航栏入口进入查询结果页
@login_required
def show_mysearchlist(request):
    searchlists = []
    # 获取当前页面的url
    current_path = request.get_full_path()
    # 验证用户是否已注册,获取用户id
    if not request.user.is_authenticated:
        return HttpResponseRedirect('library:login')
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


# 显示“我的图书馆”页面，添加图书到我的图书馆页面的代码见“library:def book_detail”
# "readerCenter:def mylib"应该完成显示我的图书馆书籍
def mylib(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('login:login')

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


# 提供删除我的图书馆内书籍的功能-未开发完毕，还需学习借书、还书实现的过程
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
        return HttpResponseRedirect('library:login')
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
        return HttpResponseRedirect('library:login')
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
