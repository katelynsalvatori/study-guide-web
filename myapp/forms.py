from django import forms
from models import Question, Answer, StudyGuide
from django.forms.models import inlineformset_factory

class CreateUserForm(forms.Form):
    user_name = forms.CharField(label='User Name', max_length=32)

class StudyGuideForm(forms.ModelForm):
    class Meta:
        model = StudyGuide
        fields = ['name']

class QuestionForm(forms.ModelForm):
    id = forms.IntegerField(min_value=0, required=True, widget=forms.HiddenInput())
    class Meta:
        model = Question
        widgets = {'id': forms.HiddenInput(), 'study_guide': forms.HiddenInput()}

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        widgets = {'id': forms.HiddenInput(), 'question': forms.HiddenInput()}