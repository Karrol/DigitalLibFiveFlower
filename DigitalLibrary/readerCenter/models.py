from django.db import models
from login.models import Reader
from search.models import book_info



class readerLibrary(models.Model):
    class Meta:
        verbose_name = '我的图书馆'
        verbose_name_plural = '我的图书馆'
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者',default='51')
    ISBN = models.ForeignKey(book_info, on_delete=models.CASCADE, verbose_name='ISBN')
    In_date = models.DateTimeField(verbose_name='加入时间',null=True,blank=True,default=None)

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
    date_issued = models.DateField(verbose_name='借出时间')
    date_due_to_returned = models.DateField(verbose_name='应还时间')
    date_returned = models.DateField(null=True, verbose_name='还书时间')
    amount_of_fine = models.FloatField(default=0.0, verbose_name='欠款')

    def __str__(self):
        return '{} 借了 {}'.format(self.reader, self.ISBN)