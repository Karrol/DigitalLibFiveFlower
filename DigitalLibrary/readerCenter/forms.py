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
        max_length=256,
        label="姓名",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'username',
            'id': 'id_username',
        })
    )
    sex = forms.ChoiceField(label='性别', choices=gender)

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