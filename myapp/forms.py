from django import forms

class CreateUserForm(forms.Form):
    user_name = forms.CharField(label='User Name', max_length=32)

class CreateStudyGuideForm(forms.Form):
    study_guide_name = forms.CharField(label='Study Guide Name', max_length=32)