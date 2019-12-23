from django.db import models
from login.models import Reader
from search.models import book_info
import django.utils.timezone as timezone


class readerLibrary(models.Model):
    class Meta:
        verbose_name = '我的图书馆'
        verbose_name_plural = '我的图书馆'
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者',default='51')
    ISBN = models.ForeignKey(book_info, on_delete=models.CASCADE, verbose_name='ISBN')
    In_date = models.DateField(verbose_name='加入时间', default = timezone.now)
    #TO DO：可以开启读者的个人图书馆管理-增删查-提供两种界面-书架界面/管理界面
    defBookType=models.CharField(verbose_name='加入时间',max_length=200,default='我的图书分区')

class readerSearchlist(models.Model):
    class Meta:
        verbose_name = '我的查询历史'
        verbose_name_plural = '我的查询历史'
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    ISBN = models.ForeignKey(book_info, on_delete=models.CASCADE, verbose_name='ISBN')
    search_date = models.DateTimeField(verbose_name='查询时间',null=True,blank=True,default=None)

#Borrowing也要迁移过来才可以

class Borrowing(models.Model):
    class Meta:
        verbose_name = '借阅'
        verbose_name_plural = '借阅'

    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    ISBN = models.ForeignKey(book_info, on_delete=models.CASCADE, verbose_name='ISBN')
    #借还书的数据是随机生成的，所以是原demo存在还书时间的
    date_issued = models.DateField(verbose_name='借出时间')
    date_due_to_returned = models.DateField(verbose_name='应还时间')
    date_returned = models.DateField(null=True, verbose_name='还书时间')
    amount_of_fine = models.FloatField(default=0.0, verbose_name='欠款')

    def __str__(self):
        return '{} 借了 {}'.format(self.reader, self.ISBN)

class adviceforSearch(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    title=models.CharField('建议主题',max_length=256,blank='False')
    advice=models.CharField('读者对系统的建议',max_length=1000,blank='False')
    inTime=models.DateField(verbose_name='建议日期')


class moneyTask(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    taskname = models.CharField('事务名称', max_length=256, blank='False')
    price = models.CharField('事务花费', max_length=1000, blank='False')
    inTime = models.DateField(verbose_name='事务发生日期')
