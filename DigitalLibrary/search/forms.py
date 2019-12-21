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
