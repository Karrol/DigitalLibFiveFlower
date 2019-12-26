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
        (u'豆瓣图书库', u'豆瓣图书库'),
        (u'四川大学图书馆书库', u'四川大学图书馆书库'),
        (u'全部数据库', u'全部数据库'),
    ]
    Format = [
        (u'非规范数据格式', u'非规范数据格式'),
        (u'标准格式', u'标准格式'),
        (u'卡片格式', u'卡片格式'),
        (u'引文格式', u'引文格式'),
    ]
    recordNumCHOICES = [
        (u'5', u'5'),
        (u'8', u'8'),
        (u'10', u'10'),
        (u'15', u'15'),
    ]
    crecordNumCHOICES = [
        (u'1', u'1'),
        (u'2', u'2'),
        (u'3', u'3'),
        (u'5', u'5'),
    ]

    recordNum=forms.IntegerField(
        max_value=20,
        min_value=5,
        label="每页显示记录数",
        widget=forms.NumberInput(

            attrs={
                'class': 'form-control input-lg',
                'name': 'recordNum',
            },

        ),
        required=False,
    )
    

    defaultLibrary = forms.CharField(
        max_length=20,
        label="默认检索分馆",
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
        label="默认规范数据格式",
        widget=forms.widgets.Select(
            choices=Format,
            attrs={
                'class': 'form-control input-lg',
                'name': 'resultFormat',
            },
        ),
        required=False,)


    


class multiKeywordsForm(forms.Form):
    book_lib_name = [ (u'豆瓣图书库', u'豆瓣图书库'),
        (u'四川大学图书馆书库', u'四川大学图书馆书库'),
        (u'全部数据库', u'全部数据库'),
                      ]

    catogary = forms.CharField(
        max_length=20,
        label="主题",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control input-lg',
                'name': 'catogary',
            }
        ),
        required=False,

    )
    author = forms.CharField(
        max_length=20,
        label="著者",
        widget=forms.TextInput(
            attrs={

                'class': 'form-control input-lg',
                'name': 'author',
            }
        ),
        required=False,

    )
    title = forms.CharField(
        max_length=20,
        label="题名",
        widget=forms.TextInput(
            attrs={

                'class': 'form-control input-lg',
                'name': 'title',
            }
        ),
        required=False,

    )
    publishYear = forms.CharField(
        max_length=20,
        label="出版年",
        widget=forms.TextInput(
            attrs={

                'class': 'form-control input-lg',
                'name': 'publishYear',
            }
        ),
        required=False,

    )
    press = forms.CharField(
        max_length=20,
        label="出版社",
        widget=forms.TextInput(
            attrs={

                'class': 'form-control input-lg',
                'name': 'press',
            }
        ),
        required=False,

    )

    booklib = forms.CharField(
        max_length=20,
        label="书目库",
        widget=forms.Select(
            choices=book_lib_name,
            attrs={

                'class': 'form-control input-lg',
                'name': 'booklib',
            }
        ),
        required=False,

    )
