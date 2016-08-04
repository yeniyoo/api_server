# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-04 08:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_auto_20160731_1506'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='roundnickname',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='roundnickname',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='roundnickname',
            name='round',
        ),
        migrations.RemoveField(
            model_name='roundnickname',
            name='user',
        ),
        migrations.AddField(
            model_name='pick',
            name='nickname',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='apps.Nickname'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='RoundNickname',
        ),
    ]
