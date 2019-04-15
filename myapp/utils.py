from difflib import SequenceMatcher
from .models import Question, Answer

"""
Normalize text to be lowercase and free of dashes for comparison
"""
def cleaned(text):
    return text.lower().replace("-", " ")

"""
Check if the two strings contain the same words
but in different orders
"""
def tokens_match(str1, str2):
    str1_tokens = str1.split(" ")
    str2_tokens = str2.split(" ")

    if len(str1_tokens) != len(str2_tokens): return False

    for str1_token in str1_tokens:
        if str1_token not in str2_tokens: return False

    for str2_token in str2_tokens:
        if str2_token not in str1_tokens: return False

    return True

"""
Find the answer from the list of possible correct answers
that is the most "similar to" the given entered answer
"""
def similar_to(answer, possible_answers):
    most_similar = None
    most_similar_ratio = 0.0

    for possible_answer in possible_answers:

        if tokens_match(answer, cleaned(possible_answer.answer_text)): return (possible_answer, 1.0)

        ratio = SequenceMatcher(None, answer, cleaned(possible_answer.answer_text)).ratio()
        if ratio > most_similar_ratio:
            most_similar = possible_answer
            most_similar_ratio = ratio

    return (most_similar, most_similar_ratio)

"""
Process the entered answers for correctness:
- An answer that matches the text of a correct answer exactly is correct
- An answer that contains the same words in a different order is correct
- An answer that has a "similarity ratio" greater than 0.5 is a partial
  match, which is marked as correct but displayed to the user
"""
def process_answers(entered_answers, correct_answers):
    num_wrong = 0
    partial_matches = []
    correct_answer_texts = [cleaned(ans.answer_text) for ans in correct_answers]
    for answer in entered_answers:
        if answer in correct_answer_texts:
            correct_answers = list(filter(lambda x: cleaned(x.answer_text) != answer, correct_answers))
            correct_answer_texts.remove(answer)
        else:
            most_similar, most_similar_ratio = similar_to(answer, correct_answers)
            if most_similar_ratio > 0.5:
                correct_answers.remove(most_similar)
                correct_answer_texts.remove(cleaned(most_similar.answer_text))
                partial_matches.append(most_similar.answer_text)
            else:
                num_wrong += 1
    return num_wrong, partial_matches

"""
Create HTML based on the given results
"""
def create_response_html(correct_answers, num_wrong, partial_matches):
    resp = ""
    if num_wrong == 0:
        resp += "<p class='correct'>Correct!</p>"
    else:
        resp += "<p class='incorrect'>Incorrect.</p>"
        resp += "<p>Correct answers:</p>"
        resp += "<ul>"

        for answer in correct_answers:
            resp += "<li>%s</li>" % answer

        resp += "</ul>"
    
    if len(partial_matches) > 0:
        resp += "<p>Partial matches:</p>"
        resp += "<ul>"

        for match in partial_matches:
            resp += "<li>%s</li>" % match

        resp += "</ul>"

    return resp

"""
Convert the QueryDict from the request to save a study guide into
a usable Python dictionary
"""
def convert_data(data):
    existing = {}
    unsaved = {}
    for key in data:
        components = key.split("-")
        value = data[key]
        if components[-1].endswith("[]"):
            value = data.getlist(key)
            components[-1] = components[-1].split("[]")[0]
        if key.startswith("existing"):
            if not components[1] in existing:
                existing[components[1]] = {}

            existing[components[1]][components[2]] = value
        else:
            if not components[1] in unsaved:
                unsaved[components[1]] = {}

            unsaved[components[1]][components[2]] = value
    return existing, unsaved

"""
Process the updates for the given study guide, given data from
the front end
"""
def process_study_guide_update(study_guide, data):
    existing, unsaved = convert_data(data)

    update_existing_questions(existing)
    add_new_questions(unsaved, study_guide)

"""
Update the data of all the existing questions in a study guide
"""
def update_existing_questions(existing_questions):
    for question_id in existing_questions:
        is_enabled = existing_questions[question_id]["enabled"] == "true"
        question_text = existing_questions[question_id]["question_text"]
        answers = existing_questions[question_id]["answer_texts"]
        question = Question.objects.get(id=question_id)

        # Update the question data and save it
        question.question_text = question_text
        question.enabled = is_enabled
        question.save()

        # Get the existing answers from the database to compare to those from the request
        existing_answers = Answer.objects.filter(question=question)
        existing_answer_texts = [x.answer_text for x in existing_answers]

        # The following two-step process for updating answers is basically a workaround
        # for not having answer ids passed through the request

        # Delete answers from the database if they're not in the HTTP request
        for answer in existing_answers:
            if answer.answer_text not in answers:
                answer.delete()

        # Create answers in the database if they don't already exist
        for answer_text in answers:
            if answer_text not in existing_answer_texts and answer_text != '':
                Answer.objects.create(answer_text=answer_text, question=question)

"""
Add new questions to a study guide
"""
def add_new_questions(unsaved_questions, study_guide):
    for question in unsaved_questions:
        is_enabled = unsaved_questions[question]["enabled"] == "true"
        question_text = unsaved_questions[question]["question_text"]
        answers = unsaved_questions[question]["answer_texts"]
        new_question = Question.objects.create(
            question_text=question_text, enabled=is_enabled, study_guide=study_guide)
        for answer in answers:
            Answer.objects.create(answer_text=answer, question=new_question)
        