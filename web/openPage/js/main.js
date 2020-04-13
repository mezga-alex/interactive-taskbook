let answers;
var correctAnswers = new Set();
var strictCheck = false;

function passAnswers(newAnswers) {
    answers = newAnswers;
}

// Resize all input forms according to their content
function resizeInputs() {
    let lexemeSpans = document.getElementsByClassName("input__label-content--kaede");
    let inputs = document.getElementsByClassName("input--kaede");
    for (var i = 0; i < lexemeSpans.length; i++) {
        let lexeme = lexemeSpans.item(i).innerHTML;
        inputs.item(i).style.width = (2 * (lexeme.length + 1) + 1).toString() + 'em';
    }
}

// Add animation class
function animateCSS(element, animationName, callback) {
    classie.addClass(element, 'animated');
    classie.addClass(element, animationName);

    function handleAnimationEnd() {
        classie.removeClass(element, 'animated');
        classie.removeClass(element, animationName);
        //node.classList.remove('animated', animationName);
        element.removeEventListener('animationend', handleAnimationEnd);

        if (typeof callback === 'function') callback()
    }

    element.addEventListener('animationend', handleAnimationEnd);
}

// e.g. taskID = 'task-3-3' means that the index of the phrase is 3, and the index of the word inside the phrase is 3
function checkAnswer(taskID, userAnswer) {
    let ids = taskID.match(/\d+/g);
    let phraseID = ids[0];
    let wordID = ids[1];
    let correctAnswer = answers[phraseID][wordID];
    return userAnswer.toUpperCase() === correctAnswer.toUpperCase();
}

// Check all words in
function checkFullTask(e) {
    let taskPhrasesIndices = $(e).attr('id').match(/\d+/g);
    for (let phraseIndex of taskPhrasesIndices) {
        var isCorrect = true;
        var wordIndex = 0;

        var taskID = '#task-' + phraseIndex.toString() + '-' + wordIndex.toString();
        //while (isCorrect && ($(taskID).length !== 0)) {
        while ($(taskID).length !== 0) {
            let userAnswer = $(taskID).val();
            isCorrect = checkAnswer(taskID, userAnswer);

            // TODO: Get element by jquery.
            //  element = $(taskID) doesn't work.
            // Get span for the current input
            spanID = 'span-'+taskID.substr(1); // Remove '#' from taskID
            var element = document.getElementById(spanID);
            // If the word is correct -> set up green background
            if (isCorrect) {
                if (!correctAnswers.has(taskID.substr(1))) {
                    correctAnswers.add(taskID.substr(1));
                    classie.removeClass(element, 'border-bottom-danger');
                    classie.addClass(element, 'border-bottom-success');
                    animateCSS(element, 'fadeIn');
                }
                // If the word is correct and is not empty -> set up red background
            } else if (userAnswer !== '') {
                if (correctAnswers.has(taskID)) correctAnswers.delete(taskID);
                classie.removeClass(element, 'border-bottom-success');
                classie.addClass(element, 'border-bottom-danger');
                animateCSS(element, 'fadeIn');
            }

            // Next ID
            wordIndex += 1;
            taskID = '#task-' + phraseIndex.toString() + '-' + wordIndex.toString();
        }
    }
}

$(document).ready(() => {
    resizeInputs();

    // Handle pressing the enter key
    var inputs = $(':input').keyup(function(e){
        // alert('key');
        if (e.which == 13) {
            e.preventDefault();
            var nextInput = inputs.get(inputs.index(this) + 1);
            if (nextInput) {
                // If the next element is an INPUT -> switch to the next input.
                if (nextInput.tagName === 'INPUT') {
                    nextInput.focus();
                }
                // If the next element is the Button -> check the task by emulating the button click.
                else {
                    let nextID = '#' + $(nextInput).attr('id');
                    $(nextID).click();

                    // If there is the next task -> go to it
                    nextInput = inputs.get(inputs.index(this) + 2).focus();
                    if (nextInput && nextInput.tagName === 'INPUT')
                        nextInput.focus();
                }
            }
        } else {
            // If there are any “correct” or “inCorrect” classes, but change the input -> delete these classes
            let taskID = $(inputs.get(inputs.index(this))).attr('id');
            // Need span to create border for full length
            let spanID = 'span-'+taskID;
            let element = document.getElementById(spanID);

            let isCorrect = element.classList.contains('border-bottom-success');
            let isIncorrect = element.classList.contains('border-bottom-danger');
            if (isCorrect || isIncorrect) {
                if (isCorrect) {
                    // Remove current input ID from correct answers
                    correctAnswers.delete(taskID);
                    classie.removeClass(element, 'border-bottom-success');
                }
                if (isIncorrect) classie.removeClass(element, 'border-bottom-danger');
                animateCSS(element, 'fadeIn');
            }
        }
    });

    // Get the button and check all related words inside the task
    $('.btn-check-task').on('click', function checkMultipleAnswers(e) {
        checkFullTask(this);
    });
});