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
from .models import book_info,book_shumu
from login.models import Reader
from readerCenter.models import Borrowing, readerLibrary
from infoCenter.models import newsArticle_info, newsColumn_info
from service.models import Intro, Category
from .forms import SearchForm ,searchParameterForm ,multiKeywordsForm
from django.db.models import Q
from django.template import loader ,Context
from django.http import HttpResponse


# Create your views here.
# 书籍的检索首页
def index(request):

    context = {
        'searchForm': SearchForm(),
    }

    return render(request, 'search/index.html', context)


# 目前首页还是测试状态
def test(request):
    #张丽：首页展示的不同种类的新闻列表，首页底部
    indexnews_queryset=[]
    index_news_column = newsColumn_info.objects.filter(newsIndexDiaplay=True)
    for colum in index_news_column:
        index_news = newsArticle_info.objects.filter(newsColumn=colum.pk)[:5]
        indexnews_queryset.append(index_news)
    
    # 李玉和 信息中心导航栏
    news_columns = newsColumn_info.objects.filter(nav_display=True)
    service_cotegories = Category.objects.filter(side_display=True)

    context = {
        'searchForm': SearchForm(),
        
        'indexnews_queryset': indexnews_queryset,
        'news_columns': news_columns,
        'service_cotegories': service_cotegories,
    }
    return render(request, 'search/index_test.html', context)


# 书籍检索结果页
def book_search(request):
    # 判断用户状态，如果是登录用户，记录其现在浏览的位置，游客则不记录
    if request.user.is_authenticated:
        request.session['user_location'] = 'search:searchBook'
    # 书籍检索功能：用户游客都可以实现
    search_by = request.GET.get('search_by', '书名')
    # 设置空列表存放要显示在前端的数据
    books = []
    current_path = request.get_full_path()
    keyword = request.GET.get('keyword', u'_书目列表')
    request.session['searchindex_keyword']=keyword
    request.session['searchindex_search_by']=search_by
    # 给books赋值
    if keyword == u'_书目列表':
        books = book_info.objects.all()
    else:
        if search_by == u'书名':
            keyword = request.GET.get('keyword', None)
            books_douban = book_info.objects.filter(title__icontains=keyword).order_by('-title')[0:100]
            books_sculib = book_shumu.objects.filter(title__icontains=keyword).order_by('-title')[0:100]
            
        elif search_by == u'ISBN':
            keyword = request.GET.get('keyword', None)
            books_douban = book_info.objects.filter(ISBN=keyword).order_by('-title')[0:100]
            books_sculib = book_shumu.objects.filter(ISBN=keyword).order_by('-title')[0:100]

        elif search_by == u'作者':
            keyword = request.GET.get('keyword', None)
            books_douban = book_info.objects.filter(author__icontains=keyword).order_by('-title')[0:100]

            books_sculib = book_shumu.objects.filter(author__icontains=keyword).order_by('-title')[0:100]

        elif search_by == u'图书目录':
            keyword = request.GET.get('keyword', None)
            books_douban = book_info.objects.filter(category__icontains=keyword).order_by('-title')[0:100]

            books_sculib = book_shumu.objects.filter(category__icontains=keyword).order_by('-title')[0:100]

        # 翻页功能实现
        elif search_by==u'模糊检索':
            keyword = request.GET.get('keyword', None)
            books_douban = book_info.objects.filter(Q(title__icontains=keyword) |
                                     Q(author__icontains=keyword) |
                                     Q(category__icontains=keyword))

            books_sculib = book_shumu.objects.filter(Q(title__icontains=keyword) |
                                                    Q(author__icontains=keyword) |
                                                    Q(category__icontains=keyword))
            
    counter = 0
    # 将从两个库中检索到的书添加到一个记录集中
    if not books:
        for book in books_douban:
            counter = counter + 1
            books.append(book)
        for book in books_sculib:
            counter = counter + 1
            books.append(book)
    paginator = Paginator(books, 5)
    page = request.GET.get('page', 1)

    try:
        # page是paginator实例对象的方法，返回第page页的实例对象，所以books是第page页的记录集
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    # ugly solution for &page=2&page=3&page=4
    # 当你已经是某一页时，current_path的最后有&page(previous),所以这里是在做清洗
    if '&page' in current_path:
        current_path = current_path.split('&page')[0]

    initial = {"search_by": request.session['searchindex_search_by'],
               'keyword': request.session['searchindex_keyword'],
               }
    context = {
        'books': books,
        'counter': counter,
        'search_by': search_by,
        'keyword': keyword,
        'current_path': current_path,
        'searchForm': SearchForm(initial),
    }
    return render(request, 'search/search.html', context)


# 书籍详情页
def book_detail(request, ISBN):
    ISBN = ISBN
    print(ISBN)
    if not ISBN:
        return HttpResponse('there is no such an ISBN')
    try:
        book = book_info.objects.filter(pk=ISBN)
        if not book:
            book=book_shumu.objects.get(pk=ISBN)
        else:
            book = book_info.objects.get(pk=ISBN)

        # 李玉和增加 阅读量自增
        book_info.increase_views(book)
    except book_info.DoesNotExist:
        return HttpResponse('there is no such an ISBN')  # end李玉和增加 阅读量自增

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
                bk.bookID.quantity -= 1
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
                return HttpResponseRedirect('/readerCenter/bowrrowing?state=borrow_success')
            else:
                state = 'upper_limit'
    context = {
        'state': state,
        'book': book,
    }
    return render(request, 'search/book_detail.html', context)


#检索参数设置
def searchparameter(request):
    response = HttpResponse('')
    searchparameter_form = searchParameterForm(request.POST)
    if request.method == "POST":
        message = '请注意检查填写内容'
        if searchparameter_form.is_valid():
           parameter = searchparameter_form.cleaned_data
           recordNum = parameter['recordNum']#每页记录数
           crecordNum = parameter['crecordNum']#自动完整显示记录数
           defaultLib = parameter['defaultLibrary']
           resultFormat = parameter['resultFormat']
           formatData = parameter['formatData']  # 自动完整显示记录数
           response.set_cookie('recordNum', recordNum)
           response.set_cookie('crecordNum', crecordNum)
           response.set_cookie('defaultLib', defaultLib)
           response.set_cookie('resultFormat', resultFormat)
           response.set_cookie('formatData', formatData)
        message = '参数设置成功！请继续检索叭！'
        context = {
            'searchparameter_form': searchparameter_form,
            'message': message,
        }
        return render(request, 'search/searchParameter.html', context)
    return render(request, 'search/searchParameter.html', locals())


def search_multikeyword(request):


    if request.method == "POST":
        multikey_form = multiKeywordsForm(request.POST)
        if multikey_form.is_valid():
           keywords = multikey_form.cleaned_data
           catogary = keywords['catogary']#每页记录数
           title = keywords['title']#每页记录数
           author = keywords['author']#自动完整显示记录数
           publishYear = keywords['publishYear']
           press = keywords['press']
           booklib = keywords['booklib']

           request.session['keyword_catogary'] = catogary
           request.session['keyword_title'] = title
           request.session['keyword_author'] = author
           request.session['keyword_publishYear'] = publishYear
           request.session['keyword_press'] = press
           request.session['keyword_booklib'] = booklib
        return redirect("search:searchHighResult")
    else:
        initial = {"catogary": request.session['keyword_catogary'],
                   "title": request.session['keyword_title'],
                   'author': request.session['keyword_author'],
                   'publishYear': request.session['keyword_publishYear'],
                   'press': request.session['keyword_press'],
                   'booklib': request.session['keyword_booklib'],
                   }
        multikey_form = multiKeywordsForm(initial)
        return render(request, "search/high_level_search.html",
                      locals())
    
    

def multisearchlist(request):
    catogary =request.session['keyword_catogary']  # 每页记录数
    title = request.session['keyword_title']  # 每页记录数
    author =request.session['keyword_author']  # 自动完整显示记录数
    publishYear = request.session['keyword_publishYear']
    press = request.session['keyword_press']
    booklib = request.session['keyword_booklib']
    # 设置空列表存放要显示在前端的数据
    books = []
    current_path = request.get_full_path()
    # 给books赋值
    if booklib == '' or booklib == '豆瓣图书':
        books = book_info.objects.filter(Q(category__icontains=catogary) &
                                         Q(author__icontains=author) &
                                         Q(press__icontains=press) &
                                         Q(title__icontains=title))
    elif booklib == '四川大学图书馆':
        books = book_shumu.objects.filter(Q(category__icontains=catogary) &
                                          Q(author__icontains=author) &
                                          Q(press__icontains=press) &
                                          Q(title__icontains=title) &
                                          Q(publishTime__icontains=publishYear))

    paginator = Paginator(books, 5)
    page = request.GET.get('page', 1)

    try:
        # page是paginator实例对象的方法，返回第page页的实例对象，所以books是第page页的记录集
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    # ugly solution for &page=2&page=3&page=4
    # 当你已经是某一页时，current_path的最后有&page(previous),所以这里是在做清洗
    if '&page' in current_path:
        current_path = current_path.split('&page')[0]

    context = {
        'books': books,
        'current_path': current_path,
    }
    return render(request, 'search/multiKeywords_result.html', context)



