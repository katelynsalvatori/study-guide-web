from django.http import HttpResponse
from django.shortcuts import render, redirect
from models import User, StudyGuide, Question, Answer

def home(request):
    users = User.objects.all()
    return render(request, '../templates/home.html', {'user_list': users})

def user(request, user_id):
    user = User.objects.get(id=user_id)
    study_guides = StudyGuide.objects.filter(owner=user)
    return render(request, '../templates/user.html', {'user': user, 'study_guide_list': study_guides})

def study_guide(request, study_guide_id):
    study_guide = StudyGuide.objects.get(id=study_guide_id)
    questions = Question.objects.filter(study_guide=study_guide_id)
    question_list = []
    for question in questions:
        entry = {
            'question': question,
            'answers': Answer.objects.filter(question_id=question.id)
        }
        question_list.append(entry)
    template_params = {
        'study_guide': study_guide,
        'question_list': question_list
    }
    return render(request, '../templates/study_guide.html', template_params)
