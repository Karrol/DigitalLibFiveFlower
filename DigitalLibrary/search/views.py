from django.shortcuts import render
import datetime
from django.utils import timezone
from django.urls import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import book_info
from login.models import Reader
from readerCenter.models import Borrowing, readerLibrary
from infoCenter.models import newsArticle_info
from service.models import Intro
from .forms import SearchForm


# Create your views here.
# 书籍的检索首页
def index(request):
    # 获取新闻公告标题（显示前十条）
    news = newsArticle_info.objects.order_by('-newsPubdate')[:10]

    # 获取读者服务条目（显示前十条）
    service = newsArticle_info.objects.order_by('-newsPubdate')[:10]

    context = {
        'searchForm': SearchForm(),
        'news': news,
        'service': service,
    }

    return render(request, 'search/index.html', context)


def test(request):
    news = newsArticle_info.objects.order_by('-newsPubdate')[:10]
    context = {
        'searchForm': SearchForm(),
        'news': news,
    }
    return render(request, 'search/index_test.html', context)


# 书籍检索结果页
def book_search(request):
    # 判断用户状态，如果是登录用户，记录其现在浏览的位置，游客则不记录
    if request.user.is_authenticated:
        request.session['user_location'] = 'search:searchBook'
    #书籍检索功能：用户游客都可以实现
    search_by = request.GET.get('search_by', '书名')
    books = []
    current_path = request.get_full_path()

    keyword = request.GET.get('keyword', u'_书目列表')

    if keyword == u'_书目列表':
        books = book_info.objects.all()
    else:
        if search_by == u'书名':
            keyword = request.GET.get('keyword', None)
            books = book_info.objects.filter(title__contains=keyword).order_by('-title')[0:50]
        elif search_by == u'ISBN':
            keyword = request.GET.get('keyword', None)
            books = book_info.objects.filter(ISBN__contains=keyword).order_by('-title')[0:50]
        elif search_by == u'作者':
            keyword = request.GET.get('keyword', None)
            books = book_info.objects.filter(author__contains=keyword).order_by('-title')[0:50]
        elif search_by == u'图书目录':
            keyword = request.GET.get('keyword', None)
            books = book_info.objects.filter(category__contains=keyword).order_by('-title')[0:50]

    paginator = Paginator(books, 5)
    page = request.GET.get('page', 1)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    # ugly solution for &page=2&page=3&page=4
    if '&page' in current_path:
        current_path = current_path.split('&page')[0]

    context = {
        'books': books,
        'search_by': search_by,
        'keyword': keyword,
        'current_path': current_path,
        'searchForm': SearchForm(),
    }
    return render(request, 'search/search.html', context)


# 书籍详情页
def book_detail(request,ISBN):
    ISBN = ISBN
    print(ISBN)
    if not ISBN:
        return HttpResponse('there is no such an ISBN')
    try:
        book = book_info.objects.get(pk=ISBN)
        
        # 李玉和增加 阅读量自增
        book_info.increase_views(book)
    except book_info.DoesNotExist:
        return HttpResponse('there is no such an ISBN')# end李玉和增加 阅读量自增

    action = request.GET.get('action', None)
    state = None

    if action == 'borrow':

        if not request.user.is_authenticated:
            state = 'no_user'
        else:
            reader = Reader.objects.get(user_id=request.user.id)
            if reader.max_borrowing > 0:
                reader.max_borrowing -= 1
                reader.save()

                bk = book_info.objects.get(pk=ISBN)
                bk.quantity -= 1
                bk.save()

                issued = datetime.date.today()
                due_to_returned = issued + datetime.timedelta(30)

                b = Borrowing.objects.create(
                    reader=reader,
                    ISBN=bk,
                    date_issued=issued,
                    date_due_to_returned=due_to_returned)

                b.save()
                state = 'success'
                return HttpResponseRedirect('/profile?state=borrow_success')
            else:
                state = 'upper_limit'

    if action == 'add_to_mylib':

        if not request.user.is_authenticated:
            state = 'no_user'
        else:
            reader = Reader.objects.get(user_id=request.user.id)
            bk = book_info.objects.get(pk=ISBN)
            bk.save()
            # 不确定数据库中是否有这个记录时要用filter筛选并且进行判断，如果直接使用get方法，数据库中不存在这条记录就会报错
            myliblist = readerLibrary.objects.filter(ISBN=ISBN, reader=reader)
            if myliblist.exists():
                state = 'repeat_add'
                return HttpResponseRedirect('/mylib?state=repeat_add')
            else:
                issued = timezone.now()

                b = readerLibrary.objects.create(
                    reader=reader,
                    ISBN=bk,
                    In_date=issued)

                b.save()
                state = 'add_success'
                return HttpResponseRedirect('/mylib?state=add_success')
    context = {
        'state': state,
        'book': book,
    }
    return render(request, 'search/book_detail.html', context)
