from django.http import HttpResponse
from django.shortcuts import render, redirect
from models import User, StudyGuide, Question, Answer
from forms import CreateUserForm, CreateStudyGuideForm

def home(request):
    users = User.objects.all()
    if request.method == 'POST':
        username = request.POST['user_name']
        new_user = User.objects.create(name=username)
        return redirect('/user/' + str(new_user.id))
    
    form = CreateUserForm()
    return render(request, '../templates/home.html', {'user_list': users, 'form': form})

def user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        study_guide_name = request.POST['study_guide_name']
        new_study_guide = StudyGuide.objects.create(name=study_guide_name, owner=user)
        return redirect('/createstudyguide/' + str(new_study_guide.id))

    study_guides = StudyGuide.objects.filter(owner=user)
    form = CreateStudyGuideForm()
    return render(request, '../templates/user.html', {'user': user, 'study_guide_list': study_guides, 'form': form})

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

def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('/')

def create_study_guide(request, study_guide_id):
    study_guide = StudyGuide.objects.get(id=study_guide_id)
    return redirect('/user/' + str(study_guide.owner.id))
