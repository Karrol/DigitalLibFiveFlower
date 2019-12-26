from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone
from login.models import Reader
# Django-taggit
from taggit.managers import TaggableManager

# 导入Image处理图片
from PIL import Image

from django.urls import reverse


# Create your models here.
# 文章栏目模型
class ArticleColumn(models.Model):
    """
    栏目的 Model
    """
    # 栏目标题
    title = models.CharField(max_length=100, blank=True)
    # 创建时间
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章栏目'
        verbose_name_plural = '文章栏目'  # 保证取消admin的model的s


# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章栏目的“一对多”外键
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 浏览量
    total_views = models.PositiveIntegerField(default=0)

    # 文章标签
    tags = TaggableManager(blank=True)

    # 文章标题图，%Y%m%d进行日期格式化,比如上传时间是2019年2月26日，则标题图会上传到media/article/20190226这个目录中。
    avatar = models.ImageField(upload_to='article/%Y%m%d/', blank=True)

    # 保存时处理图片
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(ArticlePost, self).save(*args, **kwargs)

        # 固定宽度缩放图片大小
        # 博文的标题图不是必须的，if中的self.avatar剔除掉没有标题图的文章，这些文章不需要处理图片。
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x, y) = image.size
            new_x = 400
            new_y = int(new_x * (y / x))
            # Image.ANTIALIAS表示缩放采用平滑滤波。
            resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
            resized_image.save(self.avatar.path)

        return article

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-created',)
        verbose_name = '发表文章'
        verbose_name_plural = '发表文章'  # 保证取消admin的model的s


    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('participate:article_detail', args=[self.id])

# 博文的评论
class Comment(models.Model):
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    commentbody = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = '读者评论'
        verbose_name_plural = '读者评论'  # 保证取消admin的model的s

    def __str__(self):
        return self.commentbody[:20]

# 好书推荐图书信息（表单）
class RecbooklistInfo(models.Model):
    # 图书名称
    bookName = models.CharField(max_length=50)
    # 图书作者
    bookAuthor = models.CharField(max_length=20)
    # 出版社
    bpublisher = models.CharField(max_length=30)
    # 出版时间
    bpubTime = models.CharField(blank=True,max_length=30)
    # ISBN编号
    bookISBN = models.CharField(max_length=10,blank=True)
    # 简要介绍
    bookIntroduction = models.TextField()
    # 推荐时间
    RecTime = models.DateField(default=timezone.now)
    # 推荐人
    RecName = models.ForeignKey(Reader, on_delete=models.CASCADE)
    # 推荐人身份
    RecIdentity = models.CharField(max_length=20)
    # 推荐人单位
    RecDepartment = models.CharField(max_length=50)

    def __str__(self):
        return self.bookName

    # 内部类class Meta用于给model定义元数据
    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-RecTime' 表明数据应该以倒序排列
        ordering = ('-RecTime',)
        verbose_name = '读者推荐'
        verbose_name_plural = '读者推荐'  # 保证取消admin的model的s

class ContactInfo(models.Model):
    # 部门名称
    administerName = models.CharField(max_length=50)
    # 联系电话
    telnumber = models.CharField(max_length=20)
    # 联系人
    contactsb = models.CharField(max_length=30)

    def __str__(self):
        return self.contactsb

    class Meta:

        verbose_name = '联系方式'
        verbose_name_plural = '联系方式'  # 保证取消admin的model的s
