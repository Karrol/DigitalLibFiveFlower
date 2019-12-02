from django.db import models

# Create your models here.

# coding:utf-8
#from django.db import models

#class bookInfo(models.Model):
#    title = models.CharField(u'图书', max_length=256)
#    hero = models.CharField(u'英雄', max_length=256)

#    def __unicode__(self):  # 在Pyth''on3中用 __str__ 代替 __unicode__
#        return self.title

from django import forms

class bookReser(models.Model):
    readerId = models.CharField(u'读者号', max_length=256)
    book = models.CharField(u'图书名', max_length=256)
    bookId = models.CharField(u'图书编号', max_length=256)
    returnTime = models.CharField(u'还书时间', max_length=256)
    place = models.CharField(u'地点', max_length=256)


