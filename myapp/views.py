from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, StudyGuide, Question, Answer
from random import shuffle
from . import forms
from . import utils

"""
Django view for the home page
On POST: create a new user with the name from the HTTP request and
redirect to the new user's study guide management page
On GET: render the current home page, including existing users
"""
def home(request):
    users = User.objects.all()
    if request.method == 'POST':
        username = request.POST['name']
        new_user = User.objects.create(name=username)
        return redirect('/user/' + str(new_user.id))
    
    form = forms.UserForm()
    return render(request, '../templates/home.html', {'user_list': users, 'form': form})

"""
Django view for the given user
On POST: create a new study guide with the name from the HTTP
request and redirect to the edit/create view for that study guide
On GET: render the current state for the user, including existing study guides
"""
def user(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        study_guide_name = request.POST['name']
        new_study_guide = StudyGuide.objects.create(name=study_guide_name, owner=user)
        return redirect('/editstudyguide/' + str(new_study_guide.id))

    study_guides = user.get_study_guides()
    form = forms.StudyGuideForm()
    return render(request, '../templates/user.html', {'user': user, 'study_guide_list': study_guides, 'form': form})

"""
Django view for studying the given study guide
Get the questions and answers associated with the study guide and
use them to render the study view
"""
def study_guide(request, study_guide_id):
    study_guide = StudyGuide.objects.get(id=study_guide_id)
    questions = list(study_guide.get_questions())
    shuffle(questions)
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

"""
Django view for deleting a user
"""
def delete_user(request, user_id):
    # TODO: replace url param with param in HTTP request
    User.objects.get(id=user_id).delete()
    return redirect('/')

"""
Django view for deleting a study guide
"""
def delete_study_guide(request, study_guide_id):
    # TODO: replace url param with param in HTTP request
    study_guide = StudyGuide.objects.get(id=study_guide_id)
    user_id = study_guide.owner.id
    study_guide.delete()
    return redirect('/user/' + str(user_id))

"""
Django view for deleting a question
"""
def delete_question(request, question_id):
    # TODO: replace url param with param in HTTP request
    question = Question.objects.get(id=question_id)
    study_guide = question.study_guide
    question.delete()
    return redirect('/editstudyguide/' + str(study_guide.id))

"""
Django view for deleting an answer
"""
def delete_answer(request, answer_id):
    # TODO: replace url param with param in HTTP request
    answer = Answer.objects.get(id=answer_id)
    study_guide = answer.question.study_guide
    answer.delete()
    return redirect('/editstudyguide/' + str(study_guide.id))

"""
Django view for editing a study guide
Get the current questins and answers for the study guide (if any)
Generate forms for creating new questions and answers
"""
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

"""
Django view for saving study guide data to the database
Extact the data from the POST and use it to update the database
"""
def save_study_guide(request, study_guide_id):
    study_guide = StudyGuide.objects.get(id=study_guide_id)
    data = request.POST
    question_id = data['id']
    # If there's no question id, the data is for a brand new question
    is_new_question = not question_id
    question_text = data['question_text']
    is_enabled = data['enabled'] == 'on' if 'enabled' in data else False
    answers = data.getlist('answer_text')

    # If the user tries to save a blank question, don't try to save anything
    # TODO: move this validation to the front end
    if not question_text:
        return redirect('/editstudyguide/' + str(study_guide_id))

    # For a new question, simply create the question and all the answers
    if is_new_question:
        new_question = Question.objects.create(
            question_text=question_text, enabled=is_enabled, study_guide=study_guide)
        for answer in answers:
            Answer.objects.create(answer_text=answer, question=new_question)
    else:
        question = Question.objects.get(id=question_id)

        # Update the question data and save it
        question.question_text = question_text
        question.enabled = is_enabled
        question.save()

        # Get the existing answers from the database to compare to those from the request
        existing_answers = Answer.objects.filter(question=question)
        existing_answer_texts = [x.answer_text for x in existing_answers]

        # The following two-step process for updating answers is basically a workaround
        # for not having answer ids passed through the POST

        # Delete answers from the database if they're not in the HTTP request
        for answer in existing_answers:
            if answer.answer_text not in answers:
                answer.delete()

        # Create answers in the database if they don't already exist
        for answer_text in answers:
            if answer_text not in existing_answer_texts and answer_text != '':
                Answer.objects.create(answer_text=answer_text, question=question)

    return redirect('/editstudyguide/' + str(study_guide_id))

"""
Django view for validating the correctness of the user's entered answers

TODO: Return actual data instead of HTML
"""
def validate_answers(request):
    question = Question.objects.get(id=request.GET["question_id"])
    correct_answers = question.get_answers()
    entered_answers = [utils.cleaned(ans) for ans in request.GET.getlist("answers[]")]
    num_wrong, partial_matches = utils.process_answers(entered_answers, list(correct_answers))

    resp = utils.create_response_html([ans.answer_text for ans in correct_answers], num_wrong, partial_matches)
        
    return HttpResponse(resp)
