from difflib import SequenceMatcher

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
