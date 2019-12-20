# Generated by Django 2.2 on 2019-12-19 14:06

import DjangoUeditor.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('search', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='newsColumn_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('columnName', models.CharField(max_length=20, verbose_name='栏目名')),
                ('columnSlug', models.CharField(db_index=True, max_length=200, verbose_name='栏目网址')),
                ('abstract', models.TextField(default='', verbose_name='栏目简介')),
                ('nav_display', models.BooleanField(default=False, verbose_name='导航显示')),
            ],
            options={
                'verbose_name': '新闻栏目',
                'verbose_name_plural': '新闻栏目',
                'ordering': ['columnName'],
            },
        ),
        migrations.CreateModel(
            name='weekbook_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookName', models.CharField(max_length=50, verbose_name='书名')),
                ('recTime', models.DateField(auto_now_add=True, verbose_name='推荐时间')),
                ('Rec_comment', DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='推荐语')),
                ('index_display', models.BooleanField(default=False, verbose_name='正式推荐')),
                ('ISBN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.book_info', verbose_name='ISBN')),
                ('promugator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发布者')),
            ],
            options={
                'verbose_name': '每周一书',
                'verbose_name_plural': '每周一书',
                'ordering': ['recTime'],
            },
        ),
        migrations.CreateModel(
            name='newsArticle_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newsTitle', models.CharField(max_length=256, verbose_name='标题')),
                ('newsSlug', models.CharField(max_length=200, unique=True, verbose_name='网址')),
                ('newsContent', DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='内容')),
                ('newsPubdate', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
                ('newsPublished', models.BooleanField(default=True, verbose_name='正式发布')),
                ('newsAuthor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('newsColumn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infoCenter.newsColumn_info', verbose_name='归属栏目')),
            ],
            options={
                'verbose_name': '新闻公告',
                'verbose_name_plural': '新闻公告',
            },
        ),
    ]
