from django.db import models

# Create your models here.
from django.db import models
from login.models import librarian_info

import uuid, os


def custom_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return filename


# 书籍书架信息
class bookshelf_info(models.Model):
    bookshelfID = models.CharField('书架财产编号', primary_key=True, max_length=10)
    bookshelfName = models.CharField('书架名称', max_length=50, default=u'文学I21')


# 图书实体的基本信息
class bookEntity_info(models.Model):
    
    location = models.CharField(max_length=64, default=u'图书馆1楼', verbose_name='位置')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    booksearchID = models.CharField('索书号',  max_length=10)
    bookshelfid = models.ForeignKey('bookshelf_info', on_delete=models.CASCADE)
    bookIntime = models.DateTimeField('图书入库时间')


# 抽象意义上的书的信息
class book_info(models.Model):
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'

    # 用ISBN号代表一抽象的书，这本书可能有多个实体（财产ID），放置于多个书架上，
    ISBN = models.CharField(max_length=13, primary_key=True, verbose_name='ISBN')
    # 书籍实体与ISBN号对应的书的关联,因为还没有实体书的信息，所以先不管它
    bookID = models.ForeignKey(bookEntity_info, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name='书名')
    author = models.CharField(max_length=32, verbose_name='作者')
    press = models.CharField(max_length=64, verbose_name='出版社')
    description = models.CharField(max_length=1024, default='', verbose_name='书籍简介')
    price = models.CharField(max_length=20, null=True, verbose_name='价格')
    category = models.CharField(max_length=64, default=u'文学', verbose_name='分类')
    cover = models.ImageField(blank=True, upload_to='bookcover', verbose_name='封面', default='null')
    # 这个索引是要作甚的
    index = models.CharField(max_length=16, null=True, verbose_name='索引')
    bookTranslator = models.CharField('译者', max_length=30, blank=True)

    page = models.CharField('图书页码', blank=True, max_length=255)
    

    # 李玉和增加  阅读量字段
    bookViews = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.bookViews += 1
        self.save(update_fields=['bookViews'])

    def __str__(self):
        return self.title + self.author


# 关于书籍类型的表尚未建立

class ebook_info(models.Model):
    ebookID = models.IntegerField('图书财产ID', primary_key=True)
    ebookName = models.CharField('书名', max_length=70)
    ebookAuthor = models.CharField('作者', max_length=30, blank=True)
    ebookTranslator = models.CharField('译者', max_length=30, blank=True)
    ebookPress = models.CharField('出版社', max_length=70)
    ebookIntime = models.DateTimeField('图书入库时间')
    ebookISBN = models.CharField('书的isbn号', max_length=10)
    ebookPage = models.IntegerField('图书页码', blank=True)
    ebookResource = models.CharField('电子图书资源内容的存储地址', max_length=200)


class booktype_info(models.Model):
    btID = models.CharField('图书类型ID', primary_key=True, max_length=10)
    btName = models.CharField('图书类型的名字', max_length=50)
    bookType = models.BooleanField('可外借/馆内阅读', default=True)

#四川大学图书馆的书目数据
class book_shumu(models.Model):
    id = models.IntegerField('系统ID')
    catolog = models.CharField('分类目录', max_length=255)
    title = models.CharField('题名', max_length=30)
    cover = models.CharField('封面', max_length=30, blank=True)
    libnname = models.CharField('馆藏地点', max_length=70, blank=True)
    searchID = models.CharField('索书号', max_length=70,blank=True)
    publishTime = models.CharField('出版年', max_length=10)
    Holding = models.CharField('馆藏数目',max_length=10, blank=True)
    author = models.CharField('作者', max_length=200)
    press = models.CharField('出版社', max_length=200)
    contentTable = models.CharField('目录', max_length=200)
    ISBN = models.CharField('ISBN', max_length=200, primary_key=True)
    price = models.CharField('价格', max_length=200)
    language = models.CharField('语言', max_length=200)
    publishInfo = models.CharField('发行信息', max_length=200)
    pubLocation = models.CharField('出版地点', max_length=200)
    contentBrief = models.CharField('简介', max_length=200)
    carrierMorphology = models.CharField('载体形态', max_length=200)
    banci = models.CharField('版次', max_length=200)
    page = models.CharField('页码', max_length=200)
    zaiti = models.CharField('载体', max_length=200)
    length = models.CharField('长度', max_length=200)