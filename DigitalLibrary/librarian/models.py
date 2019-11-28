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

class bookshelf_info(models.Model):
    bookshelfID= models.CharField('书架财产编号', primary_key=True, max_length=10)
    bookshelfName = models.CharField('书架名称', max_length=50)

class librarian_info(person_info):
    telNumber = models.CharField('电话', max_length=20, blank=True)
    email = models.CharField('邮箱', max_length=30, blank=True)
    idType = models.CharField('证件类型', max_length=10)
    idNumber = models.CharField('证件号码', max_length=20)

class booktype_info(models.Model):
    btID= models.CharField('图书类型ID', primary_key=True, max_length=10)
    btName = models.CharField('图书类型的名字', max_length=50)
    bookType = models.BooleanField('可外借/馆内阅读', default=True)

class book_info(models.Model):
    bookID = models.IntegerField('图书财产ID', primary_key=True)
    booksearchID = models.CharField('索书号', max_length=10)
    bookName = models.CharField('书名', max_length=70)
    bookAuthor = models.CharField('作者', max_length=30, blank=True)
    bookTranslator = models.CharField('译者', max_length=30, blank=True)
    bookPrice = models.DecimalField('书籍价格',max_digits=8,decimal_places=2)
    bookshelfid = models.ForeignKey( 'bookshelf_info', on_delete=models.CASCADE)
    bookPress = models.CharField('出版社', max_length=70)
    bookIntime=models.DateTimeField('图书入库时间')
    bookISBN= models.CharField('书的isbn号', max_length=10)
    librarian = models.ForeignKey('librarian_info',on_delete=models.CASCADE)
    bookPage = models.IntegerField('图书页码', blank=True)
    count = models.IntegerField('总数量', blank=True)
    bt = models.ForeignKey( 'booktype_info', on_delete=models.CASCADE)

class ebook_info(models.Model):
    ebookID = models.IntegerField('图书财产ID', primary_key=True)
    ebookName = models.CharField('书名', max_length=70)
    ebookAuthor = models.CharField('作者', max_length=30, blank=True)
    ebookTranslator = models.CharField('译者', max_length=30, blank=True)
    ebookPress = models.CharField('出版社', max_length=70)
    ebookIntime=models.DateTimeField('图书入库时间')
    ebookISBN= models.CharField('书的isbn号', max_length=10)
    librarian = models.ForeignKey('librarian_info',on_delete=models.CASCADE)
    ebookPage = models.IntegerField('图书页码',  blank=True)
    ebookResource = models.CharField('电子图书资源内容的存储地址', max_length=200)


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

