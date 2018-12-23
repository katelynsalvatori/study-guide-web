from django.http import HttpResponse
from django.shortcuts import render, redirect
from models import User, StudyGuide, Question, Answer
import forms

def home(request):
    users = User.objects.all()
    if request.method == 'POST':
        username = request.POST['user_name']
        new_user = User.objects.create(name=username)
        return redirect('/user/' + str(new_user.id))
    
    form = forms.CreateUserForm()
    return render(request, '../templates/home.html', {'user_list': users, 'form': form})

def user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        study_guide_name = request.POST['name']
        new_study_guide = StudyGuide.objects.create(name=study_guide_name, owner=user)
        return redirect('/editstudyguide/' + str(new_study_guide.id))

    study_guides = user.get_study_guides()
    form = forms.StudyGuideForm()
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
    context = {
        'study_guide': study_guide,
        'question_list': question_list,
        'user': study_guide.owner
    }
    return render(request, '../templates/study_guide.html', context)

def delete_user(request, user_id):
    User.objects.get(id=user_id).delete()
    return redirect('/')

def delete_study_guide(request, study_guide_id):
    study_guide = StudyGuide.objects.get(id=study_guide_id)
    user_id = study_guide.owner.id
    study_guide.delete()
    return redirect('/user/' + str(user_id))

def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    study_guide = question.study_guide
    question.delete()
    return redirect('/editstudyguide/' + str(study_guide.id))

def delete_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    study_guide = answer.question.study_guide
    answer.delete()
    return redirect('/editstudyguide/' + str(study_guide.id))

def edit_study_guide(request, study_guide_id):
    study_guide = StudyGuide.objects.get(id=study_guide_id)
    user = study_guide.owner
    question_form = forms.QuestionForm()
    answer_form = forms.AnswerForm()
    question_list = []
    for question in study_guide.get_questions():
        answers = question.get_answers()
        answer_list = [{'id': ans.id, 'form': forms.AnswerForm(instance=ans)} for ans in answers]
        entry = {
            'id': question.id,
            'question_form': forms.QuestionForm(instance=question),
            'answer_list': answer_list
        }
        question_list.append(entry)
    context = {
        'study_guide': study_guide,
        'user': user,
        'question_list': question_list,
        'question_form': question_form,
        'answer_form': answer_form
    }
    return render(request, '../templates/edit_study_guide.html', context)

def save_study_guide(request, study_guide_id):
    study_guide = StudyGuide.objects.get(id=study_guide_id)
    data = request.POST
    question_id = data['id']
    is_new_question = not question_id
    question_text = data['question_text']
    is_enabled = data['enabled'] if 'enabled' in data else False
    answers = data.getlist('answer_text')

    if not question_text:
        return redirect('/editstudyguide/' + str(study_guide_id))

    if is_new_question:
        new_question = Question.objects.create(question_text=question_text, enabled=is_enabled, study_guide=study_guide)
        for answer in answers:
            Answer.objects.create(answer_text=answer, question=new_question)
    else:
        question = Question.objects.get(id=question_id)

        question.question_text = question_text
        question.enabled = is_enabled
        question.save()

        existing_answers = Answer.objects.filter(question=question)
        existing_answer_texts = [x.answer_text for x in existing_answers]

        for answer in existing_answers:
            if answer.answer_text not in answers:
                answer.delete()

        for answer_text in answers:
            if answer_text not in existing_answer_texts and answer_text != '':
                Answer.objects.create(answer_text=answer_text, question=question)

    return redirect('/editstudyguide/' + str(study_guide_id))
