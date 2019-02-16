// JavaScript for templates/study_guide.html

var numQuestions = 0;
var numCorrect = 0;
var numValidated = 0;

/*
Display the nth question in the study guide view (where n = given number)
*/
function displayQuestion(number) {
    var elementId = "question-" + number;
    var element = document.getElementById(elementId);
    element.style.display = "";
    // Focus on and scroll to the next question
    $(element).find("input")[0].focus();
    $('html, body').animate({
        scrollTop: $("#" + elementId).offset().top
    }, 1000);
}

/*
Begin study mode by displaying the first question in the guide
If there are no questions, "finish" studying
*/
function begin(questionsLength) {
    document.getElementById("begin").style.display = "none";
    numQuestions = parseInt(questionsLength);
    if (numQuestions > 0) {
       displayQuestion("1");
    }
    else {
        finish();
    }
}

/*
Submit answers when enter is pressed in answer field
*/
function handleEnterOnAnswer(e, questionNum, questionId) {
    if (e.keyCode == 13) {
        e.preventDefault();
        handleAnswers(questionNum, questionId);
    }
}

/*
Handle the user's answers for the indicated question upon submission:
- Disable futher input for the question
- Validate the correctness of the submitted answer(s)
- Display feedback to the user of correctness
- Display the next question or "finish" studying if there are none
*/
function handleAnswers(questionNum, questionId) {
    disableInput(questionNum);
    validateAnswers(questionNum, questionId);
    if (questionNum < numQuestions) {
        displayQuestion(parseInt(questionNum) + 1);
    }
}

/*
Disable input for the given submitted question
*/
function disableInput(questionNum) {
    $(".question-" + questionNum).prop("disabled", "disabled");
}

/*
Find the inputted answers in the document for the given question
*/
function findAnswers(questionNum) {
    var enteredAnswers = $($('#' + questionNum + "-answers")[0]).find("input");
    var cleanedAnswers = [];
    for (i = 0; i < enteredAnswers.length; i++) {
        cleanedAnswers.push(enteredAnswers[i].value);
    }
    return cleanedAnswers;
}

/*
Validate the correctness of the user's submitted answers
*/
function validateAnswers(questionNum, questionId) {
    var enteredAnswers = findAnswers(questionNum);

    onSuccess = function(data) {
        if (data.includes("Correct!")) {
            numCorrect++;
        }
        numValidated++;
        if (numValidated === numQuestions) {
            finish((numCorrect / numQuestions) * 100);
        }
        document.getElementById("question-" + questionNum + "-results").innerHTML = data;
    };

    onFailure = function(jxhr, status, e) {
        alert(e);
    };

    $.ajax({
        url: "/validate/",
        type: "GET",
        data: {
            question_id: questionId,
            answers: enteredAnswers
        },
        success: onSuccess,
        error: onFailure
    });
}

/*
Finish the study session by displaying the results to the user
*/
function finish(percentCorrect) {
    var results;
    var resultsElement = document.getElementById("results");
    if (numQuestions > 0) {
        results = "Finished!<br>Correct answers: " + numCorrect +
            "/" + numQuestions + " = " + percentCorrect.toFixed(2) + "%";
    }
    else {
        results = "No questions to study! Add some by editing this study guide.";
    }
    resultsElement.innerHTML = results;
    resultsElement.style.display = "";
    $('html, body').animate({
        scrollTop: $("#results").offset().top
    }, 1000);
}