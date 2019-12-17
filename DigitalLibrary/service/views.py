# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category, Intro

def libBrief(request):
    side_cotegories = Category.objects.filter(side_display=True)
    return render(request, 'service\libBrief.html', {'side_cotegories':side_cotegories})

def serviceCategory(request, categorySlug):
    side_cotegories = Category.objects.filter(side_display=True)
    category = Category.objects.get(categorySlug=categorySlug)
    service_category_intros = Intro.objects.filter(serviceCategory=category.pk)

    return render(request, 'service\serviceCategory.html', {
        'side_cotegories': side_cotegories,
        'category':category,
        'service_category_intros':service_category_intros
    })


def serviceDetail(request, serviceSlug, pk):
    side_cotegories = Category.objects.filter(side_display=True)
    intro = Intro.objects.get(pk=pk)

    if serviceSlug != intro.serviceSlug:
        return redirect(intro, permanent=True)

    return render(request, 'service/serviceDetail.html', {
        'side_cotegories':side_cotegories,
        'intro': intro
    })

#站内搜索
def serviceSearch(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'service/serviceResult.html', {'error_msg': error_msg})

    post_list = Intro.objects.filter(serviceTitle__icontains=q)

    side_cotegories = Category.objects.filter(side_display=True)

    return render(request, 'service/serviceResult.html', {
        'side_cotegories':side_cotegories,
        'error_msg': error_msg,
        'post_list': post_list
    })