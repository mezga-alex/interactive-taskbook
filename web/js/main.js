var commonJson;
var articleObject;
var strictCheck = false;
let extensionID = chrome.runtime.id;
var server = localStorage.getItem("server");
var text = localStorage.getItem("text");
var groundTruthAnswers;
var correctAnswers;
var wrongAnswers;
var task;
var specifiedTask;
var result;
var url;
var globalStatisticsJSON;
var statID, exerciseID, specificationID;
var requestFromOutside;
function printSet(inputSet) {
    var result = '';
    for (let item of inputSet)
        result += item + ' ';
    console.log(result);
}

// Update current exercise node and indices to the node
function updateNodeAndIndices() {
    let indices = updateExerciseNode(globalStatisticsJSON, url, task, specifiedTask, result, true);
    statID = indices[0];
    exerciseID = indices[1];
    specificationID = indices[2];
}

// Restore statistics
function updateGlobalStatisticsJSON() {
    // Parse globalStatisticsJSON from localStorage
    globalStatisticsJSON = JSON.parse(localStorage.getItem("globalStatisticsJSON"));

    if (!globalStatisticsJSON) {
        // If it's empty -> try to restore from the server database
        // TODO: RECOVER '/get_data'. Now it's wrong to avoid response (Server not updated)
        //
        getDataBaseJSON(server+'/get_data', extensionID).then(function(value) {
            console.log(value,': Response received');

            // Restore the version from DB
            globalStatisticsJSON = JSON.parse(localStorage.getItem("globalStatisticsJSON"));
            // If it's empty -> create new JSON structure and send it to the server
            if (!globalStatisticsJSON.statistics) {
                console.log('Empty DB. Create new JSON');

                globalStatisticsJSON = createGlobalJSON(url, task, specifiedTask, result);
                updateDataBaseJSON(server + '/update', extensionID, globalStatisticsJSON);
            }
            // Update exercise node and indices
            updateNodeAndIndices();
            // Set restored version to the localStorage
            localStorage.setItem('globalStatisticsJSON', JSON.stringify(globalStatisticsJSON));
        }, function(reason) {
            // Error in DB! ->
            // create new JSON structure and send it to the server
            console.log(reason, ': Create new JSON');
            globalStatisticsJSON = createGlobalJSON(url, task, specifiedTask, result);
            updateDataBaseJSON(server + '/update', extensionID, globalStatisticsJSON);
            // Update exercise node and indices
            updateNodeAndIndices();
            localStorage.setItem('globalStatisticsJSON', JSON.stringify(globalStatisticsJSON));
        });
    } else {
        console.log('Restored from localStorage');
        // Do not wait response and update exercise node and indices
        updateNodeAndIndices();
        updateDataBaseJSON(server + '/update', extensionID, globalStatisticsJSON);
        localStorage.setItem('globalStatisticsJSON', JSON.stringify(globalStatisticsJSON));
    }
}

function newJSON() {
    if (!globalStatisticsJSON)
        globalStatisticsJSON = createGlobalJSON(url, task, specifiedTask, result);
    updateNodeAndIndices();
}
// Update globals for the new task
function updateGlobalParameters() {
    correctAnswers = new Set();
    wrongAnswers = new Set();

    url = localStorage.getItem("url");
    task = localStorage.getItem("task");
    specifiedTask = localStorage.getItem("specifiedTask");
    result = JSON.parse(localStorage.getItem("result"));
    requestFromOutside = localStorage.getItem("requestFromOutside");

    if (task === 'PASSIVE_VOICE' || task === 'ACTIVE_VOICE') {
        groundTruthAnswers = getResultAttribute(result, task, 'phrases');
        // newJSON();
        updateGlobalStatisticsJSON();
    }
}

// Helper function to get correct answer
function getCorrectAnswerByID(taskID) {
    let ids = taskID.match(/\d+/g);
    let phraseID = ids[0];
    let wordID = ids[1];
    return groundTruthAnswers[phraseID][wordID];
}

// Get index in flat array
function getFlatIndexByID(taskID) {
    let ids = taskID.match(/\d+/g);
    let phraseID = parseInt(ids[0]);
    let wordID = parseInt(ids[1]);

    var id = 0;
    for (let i = 0; i < phraseID; i++) {
        id += groundTruthAnswers[i].length
    }
    id += wordID;
    return id;
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
        return userAnswer.trim().toUpperCase() === correctAnswer.toUpperCase();
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
                    const wordID = getFlatIndexByID(taskID);
                    updateWordStatistics(globalStatisticsJSON, "correct",
                        statID, exerciseID, specificationID, wordID);
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
                    const wordID = getFlatIndexByID(taskID);
                    updateWordStatistics(globalStatisticsJSON, "wrong",
                        statID, exerciseID, specificationID, wordID);
                    // console.log('Update word stat');
                    // console.log(globalStatisticsJSON);
                }
            }
            // Next ID
            wordIndex += 1;
            taskID = '#task-' + phraseIndex.toString() + '-' + wordIndex.toString();
        }
    }
    // Save statistics
    localStorage.setItem('globalStatisticsJSON', JSON.stringify(globalStatisticsJSON));

    // console.log('Correct: ');
    // printSet(correctAnswers);
    // console.log('Wrong: ');
    // printSet(wrongAnswers);
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
    $('.btn-check-task').on('click', function () {
        checkFullTask(this);
    });

    // Check all exercises
    $('.btn-check-all').on('click', function () {
        $(".btn-check-task").each(function () {
            checkFullTask(this);
        });
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

                if ((taskType === task && taskSpecify === specifiedTask) && !requestFromOutside) return false;
                //  Update the task and only then reinitialize the globals
                updateTask(server, text, taskType, taskSpecify).then(function () {
                    updateGlobalParameters();
                    initializeInputHandlers();
                    initializeClassie();

                    const taskStr = idToString('#'+id);
                    changeElementContent('#tasksCardTitle', taskStr);
                }).catch(function (e) {
                    console.log(e);
                    // TODO: Update logic.
                    if (requestFromOutside) {
                        const taskStr = idToString('#'+id);
                        changeElementContent('#tasksCardTitle', taskStr);
                        noResultsVisualization();
                    } else {
                        // Do nothing if nothing is found
                        alert('No matches found');
                    }
                });
            }
        }
    });
}

$(document).ready(() => {
    // Recover variables from localstorage
    //All parameters are in the localstorage on the first call from the extension
    updateGlobalParameters();
    initializeInputHandlers();
    initializeLinkClickHandlers();
    initializeClassie();

    // If there was request outside the tasks' page -> trigger button
    if (requestFromOutside) {
        console.log('Request From Outside. ID =', requestFromOutside);
        $('#'+requestFromOutside).trigger('click');
        localStorage.setItem('requestFromOutside', '');
    } else {
        requestFromOutside = true;
        const id = '#TASK-'+task+'-'+specifiedTask;
        $(id).trigger('click');
        const taskStr = idToString(id);
        changeElementContent('#tasksCardTitle', taskStr);
    }
});