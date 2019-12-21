#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from login.models import Reader

#读者更改个人信息的表单-模型表单
class Change_reader_infoForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    name = forms.CharField(
        max_length=255,
        label="姓名",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        })
    )
    sex = forms.ChoiceField(label='性别', choices=gender)
   

    phone = forms.CharField(
        max_length=11,
        label="联系电话",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'birthdate',
                'id': 'id_birthdate',
            })
        
    )
    
    address = forms.CharField(
        max_length=255,
        label="住址",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'address',
            'id': 'id_address',
        })
    )
    
    job = (
        (1, '经理'),
        (2, '专业技术'),
        (3, '技师技工'),
        (4, '社区和个人服务'),
        (5, '文秘行政'),
        (6, '销售'),
        (7, '机械操作和驾驶类'),
        (8, '体力劳动类'),
    )
    occupation = forms.CharField(
        label='职业类别',
        max_length=10, widget=forms.widgets.Select(choices=job)
    )


class UploadImageForm(forms.ModelForm):
    """
        处理用户上传头像
    """
    class Meta:
        model = Reader
        fields = ['photo']

    labels = {
              'photo': '头像',
              }