# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField
from django.urls import reverse
from search.models import book_info


@python_2_unicode_compatible
class newsColumn_info(models.Model):
    columnName = models.CharField('栏目名', max_length=20)
    columnSlug = models.CharField('栏目网址', max_length=200, db_index=True)
    abstract = models.TextField('栏目简介', default='')

    newsIndexDiaplay = models.BooleanField('首页展示', default=False)
    nav_display = models.BooleanField('导航显示', default=False)

    def __str__(self):
        return self.columnName

    class Meta:
        verbose_name = '新闻栏目'
        verbose_name_plural = '新闻栏目'
        ordering = ['columnName']  # 按照哪个栏目排序


@python_2_unicode_compatible
class newsArticle_info(models.Model):
    newsColumn = models.ForeignKey("newsColumn_info", verbose_name='归属栏目', on_delete=models.CASCADE)

    newsTitle = models.CharField('标题', max_length=256)
    newsSlug = models.CharField('网址', max_length=200, unique=True)

    newsAuthor = models.ForeignKey('auth.User', blank=True, null=True, verbose_name='作者', on_delete=models.CASCADE)
    newsContent = UEditorField('内容', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')
    newsPubdate = models.DateTimeField('发表时间', auto_now_add=True, editable=True)

    newsPublished = models.BooleanField('正式发布', default=True)
    topDisplay = models.BooleanField('置顶', default=False)

    newsViews = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.newsViews += 1
        self.save(update_fields=['newsViews'])

    def __str__(self):
        return self.newsTitle

    class Meta:
        verbose_name = '新闻公告'
        verbose_name_plural = '新闻公告'

@python_2_unicode_compatible
class weekbook_info(models.Model):
    bookName = models.CharField('书名', max_length=50)
    recID =  models.CharField(max_length=12, verbose_name='推荐ID')
    ISBN = models.ForeignKey(book_info, on_delete=models.CASCADE, verbose_name='ISBN')
    promugator =  models.ForeignKey('auth.User', blank=True, null=True, verbose_name='发布者', on_delete=models.CASCADE)
    recTime =  models.DateField('推荐时间', auto_now_add=True, editable=True)
    Rec_comment = UEditorField('推荐语', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')

    def __str__(self):
        return self.bookName

    class Meta:
        verbose_name = '每周一书'
        verbose_name_plural = '每周一书'
        ordering = ['recTime']


@python_2_unicode_compatible
class rank_info(models.Model):
    rankName = models.CharField('排行榜名称', max_length=50)
    rankID = models.AutoField(primary_key=True)
    pubTime = models.DateField('发布时间', auto_now_add=True, editable=True)
    rankIntro = models.TextField('栏目简介', default='')
    rankDisplay = models.BooleanField('正式发布', default=True)

    def __str__(self):
        return self.rankName

    class Meta:
        verbose_name = '排行榜'
        verbose_name_plural = '排行榜'
        ordering = ['pubTime']

class rank_book(models.Model):
    bookOrder = models.IntegerField('图书序号', default='0')
    book = models.ForeignKey(book_info, on_delete=models.CASCADE)
    rank = models.ForeignKey(rank_info, on_delete=models.CASCADE)

    def __str__(self):
        return self.book.title

    class Meta:
        verbose_name = '排行榜内图书'
        verbose_name_plural = '排行榜内图书'
        ordering = ['bookOrder']

@python_2_unicode_compatible
class rec_source(models.Model):
    sourceName = models.CharField('资源名', max_length=50)
    enName =  models.CharField('资源英文名', max_length=100)
    eResource = models.CharField('电子资源', max_length=100)
    sourceIntro = UEditorField('资源简介', height=300, width=1000,
                           default=u'', blank=True, imagePath="uploads/images/",
                           toolbars='besttome', filePath='uploads/files/')
    recTime = models.DateField('发布时间', auto_now_add=True, editable=True)
    sourceDisplay = models.BooleanField('正式发布', default=True)

    def __str__(self):
        return self.sourceName

    class Meta:
        verbose_name = '资源推送'
        verbose_name_plural = '资源推送'
        ordering = ['recTime']