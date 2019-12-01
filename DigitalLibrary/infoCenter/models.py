# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField
from django.urls import reverse


@python_2_unicode_compatible
class newsColumn_info(models.Model):
    columnName = models.CharField('栏目名', max_length=20)
    columnSlug = models.CharField('栏目网址', max_length=200, db_index=True)
    abstract = models.TextField('栏目简介', default='')

    nav_display = models.BooleanField('导航显示', default=False)

    def __str__(self):
        return self.columnName

    def get_absolute_url(self):
        return reverse('newsColumn', kwargs={'columnSlug': self.columnSlug})

    class Meta:
        verbose_name = '新闻栏目'
        verbose_name_plural = '新闻栏目'
        ordering = ['columnName']  # 按照哪个栏目排序


@python_2_unicode_compatible
class newsArticle_info(models.Model):
    # id 这个是默认有的，也可以自己定义一个其它的主键来覆盖它
    # id = models.AutoField(primary_key=True)
    #张丽：你这里的外键是newsColumn_info的ID，并不是columnName，数据模型需要更改
    #或者你通过views里的news_column变量获取其主键，主键可以用PK代替，我用了第二种方法
    newsColumn = models.ForeignKey("newsColumn_info", verbose_name='归属栏目', on_delete=models.CASCADE)

    newsTitle = models.CharField('标题', max_length=256)
    newsSlug = models.CharField('网址', max_length=200, unique=True)

    newsAuthor = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者', on_delete=models.CASCADE)
    newsContent = UEditorField('内容', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')
    newsPubdate = models.DateTimeField('发表时间', auto_now_add=True, editable=True)

    newsPublished = models.BooleanField('正式发布', default=True)

    def __str__(self):
        return self.newsTitle

    def get_absolute_url(self):
        return reverse('newsDetail', kwargs={'pk': self.pk, 'newsSlug':self.newsSlug})

    class Meta:
        verbose_name = '新闻公告'
        verbose_name_plural = '新闻公告'

@python_2_unicode_compatible
class weekbook_info(models.Model):
    bookName = models.CharField('书名', max_length=50)
    bookID = models.CharField('书籍编码', max_length=10)
    promugator =  models.ForeignKey('auth.User', blank=True, null=True, verbose_name='发布者', on_delete=models.CASCADE)
    recTime =  models.DateField('推荐时间', auto_now_add=True, editable=True)
    Rec_comment = UEditorField('推荐语', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')

    now_display = models.BooleanField('本周推荐', default=False)
    past_display = models.BooleanField('历史推荐', default=False)

    def __str__(self):
        return self.bookName

    def get_absolute_url(self):
        return reverse('recBookDetail', kwargs=({'pk':self.pk, 'bookID':self.bookID}))

    class Meta:
        verbose_name = '每周一书'
        verbose_name_plural = '每周一书'

@python_2_unicode_compatible
class booktop_info(models.Model):
    number = models.AutoField('序号', primary_key=True)
    bookName = models.CharField('书名', max_length=50)
    bookAuthor =  models.CharField('作者', max_length=50)
    bookConcern = models.CharField('出版社', max_length=50)
    ISBN = models.CharField('ISBN号', max_length=50)

    pub_display = models.BooleanField('正式发布', default=False)

    def __str__(self):
        return self.bookName

    def get_absolute_url(self):
        return reverse('ranking', args=(self.pk, self.number))

    class Meta:
        verbose_name = '排行榜'
        verbose_name_plural = '排行榜'
        ordering = ['number']  # 按照哪个栏目排序