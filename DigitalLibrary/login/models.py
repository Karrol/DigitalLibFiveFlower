from django.db import models
from django.contrib.auth.models import User

import uuid, os


def custom_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return filename



class person_info(models.Model):
    """Model representing user profile ."""
    gender_choice = (
        ('male', '男'),
        ('female', '女'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='无分组数字图书馆系统用户')
    Sex = models.CharField('性别', max_length=4, choices = gender_choice )
    name = models.CharField(max_length=30,verbose_name='用户姓名')
    Password = models.CharField('密码', max_length=30)


class Reader(person_info):
    class Meta:
        verbose_name = '读者'
        verbose_name_plural = '读者'
        ordering = ['inTime']

    email = models.EmailField('邮箱', unique=True, blank=False)
    max_borrowing = models.IntegerField(default=5, verbose_name='可借数量')
    balance = models.FloatField(default=0.0, verbose_name='余额')
    photo = models.ImageField(blank=True, upload_to='readerimg', verbose_name='头像')
    inTime = models.DateField('登记日期',default='2019-12-19')
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
    gonghao=models.CharField('馆员工号', max_length=13,unique=True, blank=False)
    photo = models.ImageField(blank=True, upload_to='media/zhangli/librarian', verbose_name='头像')

#用户类型表：名称，可借数目
class readerType(models.Model):
    typeName = models.CharField('读者类型名',blank=False,max_length=13)
    bookNum = models.CharField('读者类型可借书籍',blank=False,max_length=3)