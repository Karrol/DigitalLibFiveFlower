from django.db import models

from django import forms

class bookReser(models.Model):
    readerId = models.CharField(u'读者号', max_length=256)
    book = models.CharField(u'图书名', max_length=256)
    bookId = models.CharField(u'图书编号', max_length=256)
    returnTime = models.CharField(u'还书时间', max_length=256)
    place = models.CharField(u'地点', max_length=256)


