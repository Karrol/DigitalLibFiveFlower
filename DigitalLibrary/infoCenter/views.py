# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage

from .models import newsColumn_info, newsArticle_info, weekbook_info
from search.models import book_info
from service.models import Category


#新闻
#新闻栏目简介
def newsIntro(request):
    news_intro_columns = newsColumn_info.objects.filter(nav_display = True)
    side_cotegories = Category.objects.filter(side_display=True)

    news_articles = newsArticle_info.objects.all()
    news_list = []
    for i in news_articles:
        news_list.append(i)
    paginator = Paginator(news_list, 5)

    if request.method == "GET":
        page = request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            articles = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            articles = paginator.page(paginator.num_pages)

    context = {
        'news_intro_columns': news_intro_columns,
        'side_cotegories': side_cotegories,
        'articles': articles,
    }
    return render(request, 'infoCenter/newsIntro.html',context)

# 新闻列表
def newsColumn(request, columnSlug):
    news_intro_columns = newsColumn_info.objects.filter(nav_display=True)
    side_cotegories = Category.objects.filter(side_display=True)

    news_column = newsColumn_info.objects.get(columnSlug=columnSlug)
    column_articles = newsArticle_info.objects.filter(newsColumn=news_column.pk)
    news_list = []
    for i in column_articles:
        news_list.append(i)
    paginator = Paginator(news_list, 5)

    if request.method == "GET":
        page = request.GET.get('page')
        try:
            news_column_articles = paginator.page(page)
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            news_column_articles = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            news_column_articles = paginator.page(paginator.num_pages)

    context = {
        'side_cotegories': side_cotegories,
        'news_intro_columns': news_intro_columns,
        'news_column': news_column,
        'news_column_articles': news_column_articles
    }

    return render(request, 'infoCenter/newsColumn.html', context)


# 新闻文章详情
def newsDetail(request):
    pk=request.GET.get('pk')
    newsSlug=request.GET.get('newsSlug')

    news_intro_columns = newsColumn_info.objects.filter(nav_display=True)
    side_cotegories = Category.objects.filter(side_display=True)

    news_article = newsArticle_info.objects.get(pk=pk)
    newsArticle_info.increase_views(news_article)

    current_column_news = newsArticle_info.objects.filter(newsColumn=news_article.newsColumn)[:5]

    all_article = newsArticle_info.objects.all()
    curr_article = None
    previous_index = 0
    next_index = 0
    previous_article = None
    next_article = None

    for index, article in enumerate(all_article):
        if index == 0:
            previous_index = 0
            next_index = index + 1
        elif index == len(all_article) - 1:
            previous_index = index - 1
            next_index = index
        else:
            previous_index = index - 1
            next_index = index + 1

        if article.newsSlug == newsSlug:
            curr_article = news_article
            previous_article = all_article[previous_index]
            next_article = all_article[next_index]
            break

    if newsSlug != news_article.newsSlug:
        return redirect(news_article, permanent=True)

    section_list = curr_article.newsContent.split('\n')

    context = {
        'news_intro_columns': news_intro_columns,
        'side_cotegories': side_cotegories,
        'news_article': news_article,
        'curr_article': curr_article,
        'section_list': section_list,
        'previous_article': previous_article,
        'next_article': next_article,
        'current_column_news': current_column_news
    }

    return render(request, 'infoCenter/newsDetail.html', context)


#每周一书
#每周一书列表
def recBookList(request):
    news_intro_columns = newsColumn_info.objects.filter(nav_display=True)
    side_cotegories = Category.objects.filter(side_display=True)

    now_recbook = weekbook_info.objects.all().first()
    if now_recbook:
        recbooks = weekbook_info.objects.all().exclude(recID = now_recbook.recID)
    else:
        sorry = "暂时还没有发布每周一书，先看看其他内容吧！"
        context = {
            'news_intro_columns': news_intro_columns,
            'side_cotegories': side_cotegories,
            'sorry': sorry
        }
        return render(request, 'infoCenter/infoCenter404.html', context)

    recbook_list = []
    for i in recbooks:
        recbook_list.append(i)
    paginator = Paginator(recbook_list, 5)

    if request.method == "GET":
        page = request.GET.get('page')
        try:
            past_recbooks = paginator.page(page)
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            past_recbooks = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            past_recbooks = paginator.page(paginator.num_pages)

    context = {
        'news_intro_columns': news_intro_columns,
        'side_cotegories': side_cotegories,
        'now_recbook': now_recbook,
        'past_recbooks': past_recbooks,
    }

    return render(request, 'infoCenter/recBookList.html', context)

#每周一书历史详情
def recBookDetail(request):
    pk = request.GET.get('pk')
    recID = request.GET.get('recID')

    news_intro_columns = newsColumn_info.objects.filter(nav_display=True)
    side_cotegories = Category.objects.filter(side_display=True)

    past_recbook = weekbook_info.objects.get(pk=pk)
    recbooks = weekbook_info.objects.all().exclude(recID=recID)

    recbook_list = []
    for i in recbooks:
        recbook_list.append(i)
    paginator = Paginator(recbook_list, 5)

    if request.method == "GET":
        page = request.GET.get('page')
        try:
            past_recbook_list = paginator.page(page)
        # todo: 注意捕获异常
        except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
            past_recbook_list = paginator.page(1)
        except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
            past_recbook_list = paginator.page(paginator.num_pages)

    context = {
        'news_intro_columns': news_intro_columns,
        'side_cotegories': side_cotegories,
        'past_recbook': past_recbook,
        'past_recbook_list': past_recbook_list,
    }

    return render(request, 'infoCenter/recBookHis.html', context)

#排行榜
#排行榜列表
def rankList(request):
    news_intro_columns = newsColumn_info.objects.all()
    side_cotegories = Category.objects.filter(side_display=True)

    # 根据自增的views字段进行排序，并获取最高的10条数据
    hotBook = book_info.objects.order_by("-bookViews")[0:10]

    context = {
        'news_intro_columns': news_intro_columns,
        'side_cotegories': side_cotegories,
        'hotBook': hotBook
    }

    return render(request, "infoCenter/rankList.html", context)

#站内搜索
def newsSearch(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'infoCenter/newsResult.html', {'error_msg': error_msg})

    post_list = newsArticle_info.objects.filter(newsTitle__icontains=q)

    news_intro_columns = newsColumn_info.objects.filter(nav_display=True)
    side_cotegories = Category.objects.filter(side_display=True)

    context = {
        'news_intro_columns': news_intro_columns,
        'side_cotegories': side_cotegories,
        'error_msg': error_msg,
        'post_list': post_list
    }

    return render(request, 'infoCenter/newsResult.html', context)