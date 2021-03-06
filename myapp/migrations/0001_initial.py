# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-26 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer_text', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'answers',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.CharField(max_length=256)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'questions',
            },
        ),
        migrations.CreateModel(
            name='StudyGuide',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'db_table': 'study_guides',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AddField(
            model_name='studyguide',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.User'),
        ),
        migrations.AddField(
            model_name='question',
            name='study_guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.StudyGuide'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Question'),
        ),
    ]
