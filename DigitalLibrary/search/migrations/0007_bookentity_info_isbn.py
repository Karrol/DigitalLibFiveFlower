# Generated by Django 2.2.5 on 2019-12-19 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_auto_20191219_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookentity_info',
            name='ISBN',
            field=models.CharField(default='980123456', max_length=13, verbose_name='ISBN'),
        ),
    ]
