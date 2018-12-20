# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Answer(models.Model):
    id = models.IntegerField(primary_key=True)
    answer_text = models.CharField(max_length=64)
    question = models.ForeignKey('Question')
    class Meta:
        db_table = 'answers'

class Question(models.Model):
    id = models.IntegerField(primary_key=True)
    question_text = models.CharField(max_length=256)
    study_guide = models.ForeignKey('StudyGuide')
    enabled = models.BooleanField(null=False, blank=True)
    class Meta:
        db_table = 'questions'

class StudyGuide(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    owner = models.ForeignKey('User')
    class Meta:
        db_table = 'study_guides'

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    class Meta:
        db_table = 'users'

