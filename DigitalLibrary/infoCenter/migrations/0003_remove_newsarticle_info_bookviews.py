# Generated by Django 2.2.5 on 2019-12-18 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('infoCenter', '0002_newsarticle_info_bookviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsarticle_info',
            name='bookViews',
        ),
    ]
