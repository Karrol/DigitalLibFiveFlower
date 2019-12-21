# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Intro
from infoCenter.models import newsColumn_info

def libBrief(request):
    side_cotegories = Category.objects.filter(side_display=True)
    news_intro_columns = newsColumn_info.objects.filter(nav_display=True)

    context = {
        'side_cotegories': side_cotegories,
        'news_intro_columns': news_intro_columns,
    }

    return render(request, 'service\libBrief.html', context)

def serviceCategory(request, categorySlug):
    side_cotegories = Category.objects.filter(side_display=True)
    news_intro_columns = newsColumn_info.objects.filter(nav_display=True)

    category = Category.objects.get(categorySlug=categorySlug)
    service_category_intros = Intro.objects.filter(serviceCategory=category.pk)

    context = {
        'side_cotegories': side_cotegories,
        'news_intro_columns': news_intro_columns,
        'category':category,
        'service_category_intros':service_category_intros
    }

    return render(request, 'service\serviceCategory.html', context)


def serviceDetail(request, serviceSlug, pk):
    side_cotegories = Category.objects.filter(side_display=True)
    news_intro_columns = newsColumn_info.objects.filter(nav_display=True)

    intro = Intro.objects.get(pk=pk)

    if serviceSlug != intro.serviceSlug:
        return redirect(intro, permanent=True)

    context = {
        'side_cotegories':side_cotegories,
        'news_intro_columns': news_intro_columns,
        'intro': intro
    }

    return render(request, 'service/serviceDetail.html', context)

#站内搜索
def serviceSearch(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'service/serviceResult.html', {'error_msg': error_msg})

    post_list = Intro.objects.filter(serviceTitle__icontains=q)

    side_cotegories = Category.objects.filter(side_display=True)
    news_intro_columns = newsColumn_info.objects.filter(nav_display=True)

    context = {
        'side_cotegories':side_cotegories,
        'news_intro_columns': news_intro_columns,
        'error_msg': error_msg,
        'post_list': post_list
    }

    return render(request, 'service/serviceResult.html', context)