from django import forms

class CreateUserForm(forms.Form):
    user_name = forms.CharField(label='User Name', max_length=32)

class StudyGuideNameForm(forms.Form):
    study_guide_name = forms.CharField(label='Study Guide Name', max_length=32)

class QuestionTextForm(forms.Form):
    question_text = forms.CharField(label='Question', max_length=256)
    is_enabled = forms.BooleanField(label='Enabled?', initial=True)

class AnswerTextForm(forms.Form):
    answer_text = forms.CharField(label='Answer', max_length=64)