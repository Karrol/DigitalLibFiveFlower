from django.db import models

# Create your models here.
from django.db import models
from library.models import librarian_info

import uuid, os

def custom_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return filename

#书籍书架信息
class bookshelf_info(models.Model):
    bookshelfID= models.CharField('书架财产编号', primary_key=True, max_length=10)
    bookshelfName = models.CharField('书架名称', max_length=50,default=u'文学I21')


#图书实体的基本信息
class bookEntity_info(models.Model):
    bookID = models.IntegerField('图书财产ID', primary_key=True,max_length=10)
    location = models.CharField(max_length=64, default=u'图书馆1楼', verbose_name='位置')
    quantity = models.IntegerField(default=1, verbose_name='数量')
    booksearchID = models.CharField('索书号',unique=True, max_length=10)
    bookshelfid = models.ForeignKey('bookshelf_info', on_delete=models.CASCADE)
    bookIntime = models.DateTimeField('图书入库时间')
    

#抽象意义上的书的信息
class book_info(models.Model):
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'
    #用ISBN号代表一抽象的书，这本书可能有多个实体（财产ID），放置于多个书架上，
    ISBN = models.CharField(max_length=13, primary_key=True,verbose_name='ISBN')
    # 书籍实体与ISBN号对应的书的关联,因为还没有实体书的信息，所以先不管它
    #bookID = models.ForeignKey(bookEntity_info, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name='书名')
    author = models.CharField(max_length=32, verbose_name='作者')
    press = models.CharField(max_length=64, verbose_name='出版社')
    description = models.CharField(max_length=1024, default='', verbose_name='书籍简介')
    price = models.CharField(max_length=20, null=True, verbose_name='价格')
    category = models.CharField(max_length=64, default=u'文学', verbose_name='分类')
    cover = models.ImageField(blank=True, upload_to=custom_path, verbose_name='封面',default='null')
    #这个索引是要作甚的
    index = models.CharField(max_length=16, null=True, verbose_name='索引')
    bookTranslator = models.CharField('译者', max_length=30, blank=True)
    price = models.DecimalField('书籍价格', max_digits=8, decimal_places=2)
    page = models.IntegerField('图书页码', max_length=10, blank=True)

    def __str__(self):
        return self.title + self.author

#关于书籍类型的表尚未建立