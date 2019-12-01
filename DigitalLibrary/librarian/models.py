from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns

class bookborrow_info(models.Model):
    brID= models.CharField('图书借阅事务ID', primary_key=True, max_length=8)
    bookID =models.OneToOneField('book_info',on_delete=models.CASCADE)
    ID = models.OneToOneField('person_info',on_delete=models.CASCADE)
    borrowTime = models.DateTimeField('借阅时间')
    expirationTime = models.DateTimeField('应归还时间')
    ifBack = models.BooleanField('是否归还', default=False)
    librarian = models.OneToOneField(to='librarian_info',related_name='librarian_info_bookborrow', on_delete=models.CASCADE)

class bookback_info(models.Model):
    bcID= models.CharField('图书归还事务ID', primary_key=True, max_length=8)
    bookID =models.OneToOneField('book_info',on_delete=models.CASCADE)
    ID = models.OneToOneField('person_info',on_delete=models.CASCADE)
    backTime = models.DateTimeField('借阅时间')
    librarian = models.OneToOneField(to='librarian_info',related_name='librarian_info_bookback',on_delete=models.CASCADE)

