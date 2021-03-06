# This is an auto-generated Django model module.
from __future__ import unicode_literals

from django.db import models

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    answer_text = models.CharField(max_length=64)
    question = models.ForeignKey('Question')
    class Meta:
        db_table = 'answers'

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=256)
    study_guide = models.ForeignKey('StudyGuide')
    enabled = models.BooleanField(null=False, blank=True, default=True)
    class Meta:
        db_table = 'questions'

    def get_answers(self):
        return Answer.objects.filter(question=self)

class StudyGuide(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    owner = models.ForeignKey('User')
    class Meta:
        db_table = 'study_guides'
        unique_together = ("name", "owner")

    def get_questions(self):
        return Question.objects.filter(study_guide=self).order_by('id')

    def get_enabled_questions(self):
        return Question.objects.filter(study_guide=self, enabled=True).order_by('id')

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    class Meta:
        db_table = 'users'

    def get_study_guides(self):
        return StudyGuide.objects.filter(owner=self)
