# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 07:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20160723_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='fb_id',
            field=models.CharField(max_length=250, unique=True, verbose_name='fb_id'),
        ),
    ]