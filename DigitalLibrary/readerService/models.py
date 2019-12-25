# Create your models here.
# coding:utf-8
#from django.db import models

#class bookInfo(models.Model):
#    title = models.CharField(u'图书', max_length=256)
#    hero = models.CharField(u'英雄', max_length=256)

#    def __unicode__(self):  # 在Pyth''on3中用 __str__ 代替 __unicode__
#        return self.title
from __future__ import unicode_literals
from django.db import models

from django import forms

from django.utils.encoding import python_2_unicode_compatible

from DjangoUeditor.models import UEditorField

from django.urls import reverse

class bookReser(models.Model):
    readerId = models.CharField(u'读者号', max_length=256)
    book = models.CharField(u'图书名', max_length=256)
    bookId = models.CharField(u'图书编号', max_length=256)
    returnTime = models.CharField(u'还书时间', max_length=256)
    place = models.CharField(u'地点', max_length=256)

class lectureReser(models.Model):
    readerId = models.CharField(u'读者号', max_length=256)
    email = models.CharField(u'邮箱地址', max_length=256)
    lectureName = models.CharField(u'讲座名称', max_length=256)
    speaker = models.CharField(u'主讲人', max_length=256)
    lectureTime = models.CharField(u'讲座时间', max_length=256)


@python_2_unicode_compatible
class RedSerTime(models.Model):
    # id 这个是默认有的，也可以自己定义一个其它的主键来覆盖它
    # id = models.AutoField(primary_key=True)
    redserName = models.CharField('标题', max_length=256)
    redserSlug = models.CharField('网址', max_length=200, unique=True)

    redserOperator = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='操作人员', on_delete=models.CASCADE)
    redserContent = UEditorField('内容', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')

    redserPublished = models.BooleanField('正式发布', default=True)
    redserPubdate = models.DateTimeField('发表时间', auto_now_add=True, editable=True)

    def __str__(self):
        return self.redserName

#    def get_absolute_url(self):
#        return reverse('serviceTime', args=(self.pk, self.redserSlug))

    class Meta:
        verbose_name = '读者服务'
        verbose_name_plural = '读者服务'

class CD(models.Model):
    # 书名
    title = models.CharField(u'书名',max_length=256)
    # 作者
    author = models.CharField(u'作者',max_length=256)
    # 光盘号
    cdId = models.CharField(u'光盘号',max_length=256,default='1')
    def __str__(self):
        return self.title