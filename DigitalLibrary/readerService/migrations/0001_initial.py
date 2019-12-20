# Generated by Django 2.2.5 on 2019-12-20 02:15

import DjangoUeditor.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='bookReser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('readerId', models.CharField(max_length=256, verbose_name='读者号')),
                ('book', models.CharField(max_length=256, verbose_name='图书名')),
                ('bookId', models.CharField(max_length=256, verbose_name='图书编号')),
                ('returnTime', models.CharField(max_length=256, verbose_name='还书时间')),
                ('place', models.CharField(max_length=256, verbose_name='地点')),
            ],
        ),
        migrations.CreateModel(
            name='RedSerTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redserName', models.CharField(max_length=256, verbose_name='标题')),
                ('redserSlug', models.CharField(max_length=200, unique=True, verbose_name='网址')),
                ('redserContent', DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='内容')),
                ('redserPublished', models.BooleanField(default=True, verbose_name='正式发布')),
                ('redserPubdate', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('redserOperator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='操作人员')),
            ],
            options={
                'verbose_name': '读者服务',
                'verbose_name_plural': '读者服务',
            },
        ),
    ]
