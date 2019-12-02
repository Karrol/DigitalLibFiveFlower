from django.db import models
from django.contrib.auth.models import User

import uuid, os


def custom_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return filename



class person_info(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    """Model representing user profile ."""
    ID = models.IntegerField('账户ID', primary_key=True)
    email = models.EmailField('邮箱', unique=True, max_length=30, blank=False)
    Sex = models.CharField(max_length=32, choices=gender, default="男")
    Name = models.CharField('用户名', max_length=30)
    Password = models.CharField('密码', max_length=30)


class Reader(person_info):
    class Meta:
        verbose_name = '读者'
        verbose_name_plural = '读者'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='读者')
    name = models.CharField(max_length=16, unique=True, verbose_name='姓名')
    phone = models.IntegerField(unique=True, verbose_name='电话')
    max_borrowing = models.IntegerField(default=5, verbose_name='可借数量')
    balance = models.FloatField(default=0.0, verbose_name='余额')
    photo = models.ImageField(blank=True, upload_to='/media/zhangli', verbose_name='头像')
    # <---demo数据库字段与我们设计的数据库字段分割线-->
    # readerType = models.CharField('读者类型', max_length=11,choices=(('A', '最大可借数目0'), ('B', '最大可借数目15'), ('C', '最大可借数目30')), default='A')
    # telNumber = models.CharField('电话', max_length=20, blank=True)
    inTime = models.DateField('登记日期', default='2019-11-16')
    #readertypeName = models.CharField('读者类型名称', max_length=30, blank=True, default='普通市民')
    # bookNumber = models.IntegerField('书籍上限', max_length=4)
    STATUS_CHOICES = (
        (0, 'normal'),
        (-1, 'overdue')
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
    )

    def __str__(self):
        return self.name



class librarian_info(person_info):
    phone = models.CharField('电话', max_length=20, blank=True)
    idType = models.CharField('证件类型', max_length=10)
    idNumber = models.CharField('证件号码', max_length=8)
