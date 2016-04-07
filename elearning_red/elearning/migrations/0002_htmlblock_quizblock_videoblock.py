# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 16:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HTMLBlock',
            fields=[
                ('block_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='elearning.Block')),
                ('content', models.TextField()),
            ],
            bases=('elearning.block',),
        ),
        migrations.CreateModel(
            name='QuizBlock',
            fields=[
                ('block_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='elearning.Block')),
                ('serialQuestions', models.TextField()),
            ],
            bases=('elearning.block',),
        ),
        migrations.CreateModel(
            name='VideoBlock',
            fields=[
                ('block_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='elearning.Block')),
                ('youtube', models.CharField(max_length=200)),
            ],
            bases=('elearning.block',),
        ),
    ]