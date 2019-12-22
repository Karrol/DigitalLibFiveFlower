#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import *

class SearchForm(forms.Form):
        CHOICES = [
            (u'模糊检索', u'模糊检索'),
            (u'ISBN', u'ISBN'),
            (u'书名', u'书名'),
            (u'作者', u'作者'),
            (u'图书目录', u'图书目录')
        ]

        search_by = forms.CharField(max_length=10,widget=forms.widgets.Select(choices=CHOICES))

        keyword = forms.CharField(
            label='',
            max_length=32,
            widget=forms.TextInput(attrs={
                'class': 'form-control input-lg',
                'placeholder': u'请输入图书信息，如书名、作者、分类......',
                'name': 'keyword',
            })
        )


class searchParameterForm(forms.Form):
    libCHOICES = [
        (u'成都青羊区分馆', u'成都青羊区分馆'),
        (u'成都武侯区分馆', u'成都武侯区分馆'),
    ]
    Format = [
        (u'标准格式', u'标准格式'),
        (u'卡片格式', u'卡片格式'),
        (u'引文格式', u'引文格式'),
    ]

    recordNum=forms.IntegerField(
        max_value=30,
        min_value=1,
        label="每页显示记录数：",
        widget=forms.NumberInput(
           
            attrs={

                'class': 'form-control input-lg',
                'name': 'recordNum',
            },
            
        ) ,
        required=False,
    )
    crecordNum = forms.IntegerField(
        max_value=10,
        min_value=1,
        label="自动显示完整记录数：",
        widget=forms.NumberInput(
            attrs={
                
                'class': 'form-control input-lg',
                'name': 'crecordNum',
            }
        ) ,
        required=False,
    )

    defaultLibrary = forms.CharField(
        max_length=20,
        label="默认检索分馆：",
        widget=forms.widgets.Select(
            choices=libCHOICES,
            attrs={
                'class': 'form-control input-lg',
                'name': 'defaultLibrary',
            },
            
        ),
        required=False,)
    resultFormat = forms.CharField(
        max_length=20,
        label="检索结果格式：",
        widget=forms.widgets.Select(
            choices=Format,
            attrs={
                'class': 'form-control input-lg',
                'name': 'resultFormat',
            },
        ),
        required=False,)


    formatData = forms.CharField(
        max_length=1,
        label= "是否出现规范数据：",
        widget=forms.widgets.CheckboxInput(
            attrs={

                'class': 'form-control input-lg',
                'name': 'formatData',
            } 
        ),
        required=False,
        
    )