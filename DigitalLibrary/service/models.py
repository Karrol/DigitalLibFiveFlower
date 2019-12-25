# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from DjangoUeditor.models import UEditorField

from django.urls import reverse


@python_2_unicode_compatible
class Category(models.Model):
    categoryName = models.CharField('类别名称', max_length=256)
    categorySlug = models.CharField('类别网址', max_length=256, db_index=True)

    side_display = models.BooleanField('导航显示', default=False)

    def __str__(self):
        return self.categoryName

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = '类别'
        ordering = ['categoryName']  # 按照哪个栏目排序


@python_2_unicode_compatible
class Intro(models.Model):
    # id 这个是默认有的，也可以自己定义一个其它的主键来覆盖它
    # id = models.AutoField(primary_key=True)
    serviceCategory = models.ForeignKey("Category", verbose_name='归属类别', on_delete = models.CASCADE)

    serviceTitle = models.CharField('标题', max_length=256)
    serviceSlug = models.CharField('网址', max_length=200, unique=True)

    serviceAuthor = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者', on_delete=models.CASCADE)
    serviceContent = UEditorField('内容', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')

    servicePublished = models.BooleanField('正式发布', default=True)
    servicePubdate = models.DateTimeField('发表时间', auto_now_add=True, editable=True)

    def __str__(self):
        return self.serviceTitle

    class Meta:
        verbose_name = '服务指南'
        verbose_name_plural = '服务指南'