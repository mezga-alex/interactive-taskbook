let answers;
var correctAnswers = new Set();
var strictCheck = false;

function passAnswers(newAnswers) {
    answers = newAnswers;
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
            // Get element of the input
            taskID = taskID.substr(1); // Remove '#'
            var element = document.getElementById(taskID);
            // If the word is correct -> set up green background
            if (isCorrect) {
                if (!correctAnswers.has(taskID)) {
                    correctAnswers.add(taskID);
                    classie.removeClass(element, 'input__field--kaede-incorrect');
                    classie.addClass(element, 'input__field--kaede-correct');
                    animateCSS(element, 'fadeIn');
                }
                // If the word is correct and is not empty -> set up red background
            } else if (userAnswer !== '') {
                if (correctAnswers.has(taskID)) correctAnswers.delete(taskID);
                classie.removeClass(element, 'input__field--kaede-correct');
                classie.addClass(element, 'input__field--kaede-incorrect');
                animateCSS(element, 'fadeIn');
            }

            // Next ID
            wordIndex += 1;
            taskID = '#task-' + phraseIndex.toString() + '-' + wordIndex.toString();
        }
    }
}

$(document).ready(() => {
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
            let isCorrect = this.classList.contains('input__field--kaede-correct');
            let isIncorrect = this.classList.contains('input__field--kaede-incorrect');
            if (isCorrect || isIncorrect) {
                if (isCorrect) {
                    // Remove current input ID from correct answers
                    let inputID = $(inputs.get(inputs.index(this))).attr('id');
                    correctAnswers.delete(inputID);
                    classie.removeClass(this, 'input__field--kaede-correct');
                }
                if (isIncorrect) classie.removeClass(this, 'input__field--kaede-incorrect');
                animateCSS(this, 'fadeIn');
            }
        }
    });

    // Get the button and check all related words inside the task
    $('.btn-check-task').on('click', function checkMultipleAnswers(e) {
        checkFullTask(this);
    });
});