#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from library.models import Reader

#读者更改个人信息的表单-模型表单
class Change_reader_infoForm(forms.ModelForm):
    #步骤1：添加模型外的表单字段
    #此处无

    #步骤2：模型与表单设置
    class Meta:
        #绑定模型，必选
        model = Reader
        #设置转换字段，必选，属性值为'__all__'时全部转换
        #fields = '__all__'
        fields = ['name','photo','email','idType','idNumber']
        #禁止模型转换的字段，可选，若设置了该属性，fields则可以不设置
        exclude = ['user','phone','max_borrowing','balance','status','intTime','readertypeName']
        #设置HTML元素控件的label标签，可选
        labels = {'name':'姓名',
                  'email':'邮箱',
                  'idType':'证件类型',
                  'idNumber':'证件号码',
                  'photo': '头像',
            }
        #定义字段的类型，可选，默认时自动转换的
        field_classes = {
            'name': forms.CharField,
            }
        #设置提示信息
        help_texts = {
            'name':'',
            }
        #自定义错误信息
        error_messages = {
            #设置全部错误信息
            '__all__':{'required':'请输入内容',
                       'invalid':'请检查输入内容'},
            #设置某个字段的错误信息
            'weight':{'required':'请输入重量数值',
                      'invalid':'请检查数值是否正确'},
            }

    #步骤3： 自定义表单字段的数据清洗
    def clean_weight(self):
        #获取字段weight的值
        idnumber = self.cleaned_data['idNumber']
        return idnumber