from django.http import HttpResponse
from django.shortcuts import render, redirect
from models import User, StudyGuide, Question, Answer
from forms import CreateUserForm, StudyGuideNameForm, QuestionTextForm, AnswerTextForm

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
        return redirect('/editstudyguide/' + str(new_study_guide.id))

    study_guides = user.get_study_guides()
    form = StudyGuideNameForm()
    return render(request, '../templates/user.html', {'user': user, 'study_guide_list': study_guides, 'form': form})

def study_guide(request, study_guide_id):
    study_guide = StudyGuide.objects.get(id=study_guide_id)
    questions = study_guide.get_questions()
    question_list = []
    for question in questions:
        entry = {
            'question': question,
            'answers': question.get_answers()
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

def edit_study_guide(request, study_guide_id):
    study_guide = StudyGuide.objects.get(id=study_guide_id)
    user = study_guide.owner
    question_text_form = QuestionTextForm()
    answer_text_form = AnswerTextForm()
    question_list = []
    for question in study_guide.get_questions():
        answers = question.get_answers()
        answer_forms = list(map(lambda x: AnswerTextForm(initial={'answer_text': x.answer_text}), answers))
        entry = {
            'question': question,
            'question_form': QuestionTextForm(initial={'question_text': question.question_text, 'is_enabled': question.enabled}),
            'answers': answers,
            'answer_forms': answer_forms
        }
        question_list.append(entry)
    template_params = {
        'study_guide': study_guide,
        'user': user,
        'question_list': question_list,
        'question_form': question_text_form,
        'answer_form': answer_text_form
    }
    return render(request, '../templates/edit_study_guide.html', template_params)
