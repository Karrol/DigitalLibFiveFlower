from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns
class person_info(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    Sex = models.CharField(max_length=32, choices=gender, default="男")
    Name = models.CharField(max_length=128, unique=True, primary_key=True)
    Password = models.CharField(max_length=256)


class reader_info(person_info):
    telNumber = models.CharField('电话', max_length=20,blank=True)
    email = models.EmailField(unique=True)
    readertypeName = models.CharField('读者类型名称', max_length=30, blank=True)
    bookNumber = models.IntegerField('书籍上限')

class bookborrow_info(models.Model):
    brID= models.CharField('图书借阅事务ID', primary_key=True, max_length=8)
    bookID =models.OneToOneField('search.book_info',on_delete=models.CASCADE)
    ID = models.OneToOneField('login.Reader',on_delete=models.CASCADE)
    borrowTime = models.DateTimeField('借阅时间')
    expirationTime = models.DateTimeField('应归还时间')
    ifBack = models.BooleanField('是否归还', default=False)
    librarian = models.OneToOneField(to='login.librarian_info',related_name='librarian_info_bookborrow', on_delete=models.CASCADE)

class bookback_info(models.Model):
    bcID= models.CharField('图书归还事务ID', primary_key=True, max_length=8)
    bookID =models.OneToOneField('search.book_info',on_delete=models.CASCADE)
    ID = models.OneToOneField('login.Reader',on_delete=models.CASCADE)
    backTime = models.DateTimeField('借阅时间')
    librarian = models.OneToOneField(to='login.librarian_info',related_name='librarian_info_bookback',on_delete=models.CASCADE)

