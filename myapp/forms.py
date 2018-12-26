from django import forms
from .models import Question, Answer, StudyGuide, User
from django.forms.models import inlineformset_factory

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'autocomplete': 'off'})}

class StudyGuideForm(forms.ModelForm):
    class Meta:
        model = StudyGuide
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'autocomplete': 'off'})}

class QuestionForm(forms.ModelForm):
    id = forms.IntegerField(min_value=0, required=True, widget=forms.HiddenInput())
    class Meta:
        model = Question
        fields = ['id', 'study_guide', 'question_text', 'enabled']
        widgets = {
            'id': forms.HiddenInput(),
            'study_guide': forms.HiddenInput(),
            'question_text': forms.TextInput(attrs={'autocomplete':'off'})
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'answer_text']
        widgets = {
            'id': forms.HiddenInput(),
            'question': forms.HiddenInput(),
            'answer_text': forms.TextInput(attrs={'autocomplete':'off'})
        }