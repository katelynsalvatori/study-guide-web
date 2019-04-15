addedQuestions = 0;

/*
Add a question field to the study guide edit view
*/
function addQuestionField() {
    addedQuestions += 1;
    var divId = "new-question-" + addedQuestions;
    var formId = "new-question-form-" + addedQuestions;

    var formTemplate = document.getElementById("new-question-form");
    var inner = formTemplate.innerHTML;

    var newElement = document.createElement('form');
    newElement.id = formId;
    newElement.innerHTML = inner;
    
    var innerDiv = newElement.children[1];
    innerDiv.id = divId;
    innerDiv.className = "unsaved-question";
    
    newElement.children[2].onclick = function() {
        addAnswerField(divId);
    };

    newElement.children[1].querySelectorAll("a")[0].onclick = function() {
        removeField(formId);
    };

    document.getElementById("new-questions").appendChild(newElement);
}

/*
Remove the element with the given ID from the page
*/
function removeField(divId) {
    var div = document.getElementById(divId);
    div.parentNode.removeChild(div);
}

/*
Maps the given function onto each element of the given list
*/
function map(list, func) {
    var result = [];
    for (var i = 0; i < list.length; i++) {
        result[i] = func(list[i]);
    }
    return result;
}

/*
Collects the contents of the study guide and sends it to the backend to be saved
*/
function saveStudyGuide(studyGuideId) {
    var existingQuestions = document.getElementsByClassName("existing-question");
    var unsavedQuestions = document.getElementsByClassName("unsaved-question");

    var unsavedQuestionsData = [];

    data = {};

    for (var i = 0; i < existingQuestions.length; i++) {
        var questionId = existingQuestions[i].id.split("-");
        questionId = questionId[questionId.length - 1];
        var questionText = existingQuestions[i].querySelector("input[name='question_text']").value;
        var isEnabled = existingQuestions[i].querySelector("input[name='enabled']").checked;
        var answerTexts = existingQuestions[i].querySelectorAll("input[name='answer_text']");
        answerTexts = map(answerTexts, x => x.value);

        data["existing-" + questionId + "-question_text"] = questionText;
        data["existing-" + questionId + "-enabled"] = isEnabled;
        data["existing-" + questionId + "-answer_texts"] = answerTexts;
    }

    for (var i = 0; i < unsavedQuestions.length; i++) {
        var questionText = unsavedQuestions[i].querySelector("input[name='question_text']").value;
        var isEnabled = unsavedQuestions[i].querySelector("input[name='enabled']").checked;
        var answerTexts = unsavedQuestions[i].querySelectorAll("input[name='answer_text']");
        answerTexts = map(answerTexts, x => x.value);

        data["unsaved-" + i + "-question_text"] = questionText;
        data["unsaved-" + i + "-enabled"] = isEnabled;
        data["unsaved-" + i + "-answer_texts"] = answerTexts;
    }

    var onSuccess = function() {
        $("#successful").show().delay(2500).fadeOut();
    };

    var onFailure = function(jxhr, status, e) {
        alert(e);
    };

    $.ajax({
        url: "/savestudyguide/" + studyGuideId + "/",
        type: "POST",
        data: JSON.stringify(data),
        success: onSuccess,
        error: onFailure
    });
}
