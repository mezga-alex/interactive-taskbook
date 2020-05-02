var strictCheck = false;
var server = localStorage.getItem("server");
var text = localStorage.getItem("text");
var groundTruthAnswers;
var correctAnswers;
var wrongAnswers;
var task;
var specifiedTask;
var result;

function printSet(inputSet) {
    var result = '';
    for (let item of inputSet)
        result += item + ' ';
    console.log(result);
}

function updateGlobalParameters() {
    correctAnswers = new Set();
    wrongAnswers = new Set();

    task = localStorage.getItem("task");
    specifiedTask = localStorage.getItem("specifiedTask");
    result = JSON.parse(localStorage.getItem("result"));

    if (task === 'PASSIVE_VOICE' || task === 'ACTIVE_VOICE') {
        groundTruthAnswers = getResultAttribute(result, task, 'phrases');
    }
}

// Helper function to get correct answer
function getCorrectAnswerByID(taskID) {
    let ids = taskID.match(/\d+/g);
    let phraseID = ids[0];
    let wordID = ids[1];
    return groundTruthAnswers[phraseID][wordID];
}

// Resize all input forms according to their content
function resizeInputs() {
    let lexemeSpans = document.getElementsByClassName("input__label-content--kaede");
    let inputs = document.getElementsByClassName("input--kaede");
    for (var i = 0; i < lexemeSpans.length; i++) {
        let lexeme = lexemeSpans.item(i).innerHTML;
        inputs.item(i).style.width = (2 * (lexeme.length + 2) + 1).toString() + 'em';
    }
}

// Add animation class
function animateCSS(element, animationName, callback) {
    classie.addClass(element, 'animated');
    classie.addClass(element, animationName);

    function handleAnimationEnd() {
        classie.removeClass(element, 'animated');
        classie.removeClass(element, animationName);
        element.removeEventListener('animationend', handleAnimationEnd);

        if (typeof callback === 'function') callback()
    }

    element.addEventListener('animationend', handleAnimationEnd);
}

// e.g. taskID = 'task-3-3' means that the index of the phrase is 3, and the index of the word inside the phrase is 3
function checkAnswer(taskID, userAnswer) {
    if (userAnswer.length !== 0) {
        let correctAnswer = getCorrectAnswerByID(taskID).replace(/\s/g, '');
        userAnswer = userAnswer.replace(/\s/g, '');
        return userAnswer.toUpperCase() === correctAnswer.toUpperCase();
    }
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
            let inputElement = $(taskID);
            let userAnswer = inputElement.val();
            isCorrect = checkAnswer(taskID, userAnswer);

            // TODO: Get element by jquery.
            //  element = $(taskID) doesn't work.
            // Get span for the current input
            taskID = taskID.substr(1); // Remove '#' from taskID
            let spanID = 'span-' + taskID;
            var element = document.getElementById(spanID);
            // If the word is correct -> set up green background
            if (isCorrect) {
                // Set correct case of answer
                inputElement.val(getCorrectAnswerByID(taskID));

                if (wrongAnswers.has(taskID)) wrongAnswers.delete(taskID);
                if (!correctAnswers.has(taskID)) {
                    correctAnswers.add(taskID);
                    classie.removeClass(element, 'border-bottom-danger');
                    classie.addClass(element, 'border-bottom-success');
                    animateCSS(element, 'fadeIn');
                }
            }
            // If the word is correct and is not empty -> set up red background
            else {
                if (correctAnswers.has(taskID)) correctAnswers.delete(taskID);
                if (userAnswer !== '') {
                    if (!wrongAnswers.has(taskID)) {
                        wrongAnswers.add(taskID);
                        classie.removeClass(element, 'border-bottom-success');
                        classie.addClass(element, 'border-bottom-danger');
                        animateCSS(element, 'fadeIn');
                    }
                }
            }
            // Next ID
            wordIndex += 1;
            taskID = '#task-' + phraseIndex.toString() + '-' + wordIndex.toString();
        }
    }
    console.log('Correct: ');
    printSet(correctAnswers);
    console.log('Wrong: ');
    printSet(wrongAnswers);
}

function initializeInputHandlers() {
    // Handle pressing the enter key
    var inputs = $(':input').keyup(function (e) {
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
            let spanID = 'span-' + taskID;
            let element = document.getElementById(spanID);

            let isCorrect = element.classList.contains('border-bottom-success');
            let isIncorrect = element.classList.contains('border-bottom-danger');
            if (isCorrect || isIncorrect) {
                if (isCorrect) {
                    // Remove current input ID from correct answers
                    correctAnswers.delete(taskID);
                    classie.removeClass(element, 'border-bottom-success');
                }
                if (isIncorrect) {
                    wrongAnswers.delete(taskID);
                    classie.removeClass(element, 'border-bottom-danger');
                }
                animateCSS(element, 'fadeIn');
            }
        }
    });

    // Get the button and check all related words inside the task
    $('.btn-check-task').on('click', function checkMultipleAnswers(e) {
        checkFullTask(this);
    });
}

function initializeLinkClickHandlers() {
    $('a').on('click', function isUpdateTask(e) {
        let id = $(this).attr('id');
        if (id) {
            let idAttributes = id.split('-');
            if (idAttributes[0] === 'TASK') {
                let taskType = idAttributes[1];
                let taskSpecify = idAttributes[2];

                if (taskType === task && taskSpecify === specifiedTask) return false;
                //  Update the task and only then reinitialize the globals
                updateTask(server, text, taskType, taskSpecify).then(function () {
                    updateGlobalParameters();
                    initializeInputHandlers();
                    initializeClassie();

                }).catch(function () {
                    // Do nothing if nothing is found
                    alert('No matches found');
                });
            }
        }
    });
}

$(document).ready(() => {
    // Recover variables from localstorage
    //All parameters are in the localstorage on the first call from the extension
    updateGlobalParameters();

    // If we have correct answers- handle it
    createTaskByResult(task, result);

    initializeInputHandlers();
    initializeLinkClickHandlers();

    initializeClassie();
});