# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-15 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0009_auto_20160415_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageblock',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='media'),
        ),
    ]