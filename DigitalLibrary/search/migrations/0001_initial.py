# Generated by Django 2.2 on 2019-12-19 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bookshelf_info',
            fields=[
                ('bookshelfID', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='书架财产编号')),
                ('bookshelfName', models.CharField(default='文学I21', max_length=50, verbose_name='书架名称')),
            ],
        ),
        migrations.CreateModel(
            name='booktype_info',
            fields=[
                ('btID', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='图书类型ID')),
                ('btName', models.CharField(max_length=50, verbose_name='图书类型的名字')),
                ('bookType', models.BooleanField(default=True, verbose_name='可外借/馆内阅读')),
            ],
        ),
        migrations.CreateModel(
            name='ebook_info',
            fields=[
                ('ebookID', models.IntegerField(primary_key=True, serialize=False, verbose_name='图书财产ID')),
                ('ebookName', models.CharField(max_length=70, verbose_name='书名')),
                ('ebookAuthor', models.CharField(blank=True, max_length=30, verbose_name='作者')),
                ('ebookTranslator', models.CharField(blank=True, max_length=30, verbose_name='译者')),
                ('ebookPress', models.CharField(max_length=70, verbose_name='出版社')),
                ('ebookIntime', models.DateTimeField(verbose_name='图书入库时间')),
                ('ebookISBN', models.CharField(max_length=10, verbose_name='书的isbn号')),
                ('ebookPage', models.IntegerField(blank=True, verbose_name='图书页码')),
                ('ebookResource', models.CharField(max_length=200, verbose_name='电子图书资源内容的存储地址')),
            ],
        ),
        migrations.CreateModel(
            name='bookEntity_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(default='图书馆1楼', max_length=64, verbose_name='位置')),
                ('quantity', models.IntegerField(default=1, verbose_name='数量')),
                ('booksearchID', models.CharField(max_length=10, verbose_name='索书号')),
                ('bookIntime', models.DateTimeField(verbose_name='图书入库时间')),
                ('bookshelfid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.bookshelf_info')),
            ],
        ),
        migrations.CreateModel(
            name='book_info',
            fields=[
                ('ISBN', models.CharField(max_length=13, primary_key=True, serialize=False, verbose_name='ISBN')),
                ('title', models.CharField(max_length=128, verbose_name='书名')),
                ('author', models.CharField(max_length=32, verbose_name='作者')),
                ('press', models.CharField(max_length=64, verbose_name='出版社')),
                ('description', models.CharField(default='', max_length=1024, verbose_name='书籍简介')),
                ('price', models.CharField(max_length=20, null=True, verbose_name='价格')),
                ('category', models.CharField(default='文学', max_length=64, verbose_name='分类')),
                ('cover', models.ImageField(blank=True, default='null', upload_to='bookcover', verbose_name='封面')),
                ('index', models.CharField(max_length=16, null=True, verbose_name='索引')),
                ('bookTranslator', models.CharField(blank=True, max_length=30, verbose_name='译者')),
                ('page', models.CharField(blank=True, max_length=255, verbose_name='图书页码')),
                ('bookViews', models.PositiveIntegerField(default=0)),
                ('bookID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.bookEntity_info')),
            ],
            options={
                'verbose_name': '图书',
                'verbose_name_plural': '图书',
            },
        ),
    ]
