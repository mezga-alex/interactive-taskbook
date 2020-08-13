export const state = {
    extensionID: chrome.runtime.id,
    server: localStorage.getItem("state.server"),
    text: localStorage.getItem("state.text"),
    groundTruthAnswers,
    correctAnswers,
    wrongAnswers,
    task,
    specifiedTask,
    result,
    url,
    globalStatisticsJSON,
    statID,
    exerciseID,
    specificationID,
    requestFromOutside,
}

// function printSet(inputSet) {
//     var state.result = '';
//     for (let item of inputSet)
//         state.result += item + ' ';
//     console.log(state.result);
// }

// Update current exercise node and indices to the node
function updateNodeAndIndices() {
    let indices = updateExerciseNode(state.globalStatisticsJSON, state.url, state.task, state.specifiedTask, state.result, true);
    state.statID = indices[0];
    state.exerciseID = indices[1];
    state.specificationID = indices[2];
}

// Restore statistics
function updateGlobalStatisticsJSON() {
    // Parse state.globalStatisticsJSON from localStorage
    state.globalStatisticsJSON = JSON.parse(localStorage.getItem("globalStatisticsJSON"));

    if (!state.globalStatisticsJSON) {
        // If it's empty -> try to restore from the state.server database
        // TODO: RECOVER '/get_data'. Now it's wrong to avoid response (state.server not updated)
        //
        getDataBaseJSON(state.server+'/db/get_data', state.extensionID).then(function(value) {
            console.log(value,': Response received');

            // Restore the version from DB
            state.globalStatisticsJSON = JSON.parse(localStorage.getItem("globalStatisticsJSON"));
            // If it's empty -> create new JSON structure and send it to the state.server
            if (!state.globalStatisticsJSON.statistics) {
                console.log('Empty DB. Create new JSON');

                state.globalStatisticsJSON = createGlobalJSON(state.url, state.task, state.specifiedTask, state.result);
                updateDataBaseJSON(state.server + '/db/update', extensionID, state.globalStatisticsJSON);
            }
            // Update exercise node and indices
            updateNodeAndIndices();
            // Set restored version to the localStorage
            localStorage.setItem('globalStatisticsJSON', JSON.stringify(state.globalStatisticsJSON));
        }, function(reason) {
            // Error in DB! ->
            // create new JSON structure and send it to the state.server
            console.log(reason, ': Create new JSON');
            state.globalStatisticsJSON = createGlobalJSON(state.url, state.task, state.specifiedTask, state.result);
            updateDataBaseJSON(state.server + '/db/update', extensionID, state.globalStatisticsJSON);
            // Update exercise node and indices
            updateNodeAndIndices();
            localStorage.setItem('globalStatisticsJSON', JSON.stringify(state.globalStatisticsJSON));
        });
    } else {
        console.log('Restored from localStorage');
        // Do not wait response and update exercise node and indices
        updateNodeAndIndices();
        updateDataBaseJSON(state.server + '/db/update', extensionID, state.globalStatisticsJSON);
        localStorage.setItem('globalStatisticsJSON', JSON.stringify(state.globalStatisticsJSON));
    }
}

function newJSON() {
    if (!state.globalStatisticsJSON)
        state.globalStatisticsJSON = createGlobalJSON(state.url, state.task, state.specifiedTask, state.result);
    updateNodeAndIndices();
}

// Update globals for the new state.task
function updateGlobalParameters() {
    state.correctAnswers = new Set();
    state.wrongAnswers = new Set();

    // state.url = localStorage.getItem("state.url");
    // state.task = localStorage.getItem("state.task");
    // state.specifiedTask = localStorage.getItem("state.specifiedTask");
    // state.result = JSON.parse(localStorage.getItem("state.result"));
    // state.requestFromOutside = localStorage.getItem("state.requestFromOutside");

    if (state.task === 'PASSIVE_VOICE' || state.task === 'ACTIVE_VOICE') {
        state.groundTruthAnswers = getResultAttribute(state.result, state.task, 'phrases');
        // newJSON();
        updateGlobalStatisticsJSON();
    }
}

// Helper function to get correct answer
function getCorrectAnswerByID(taskID) {
    let ids = taskID.match(/\d+/g);
    let phraseID = ids[0];
    let wordID = ids[1];
    return state.groundTruthAnswers[phraseID][wordID];
}

// Get index in flat array
function getFlatIndexByID(taskID) {
    let ids = taskID.match(/\d+/g);
    let phraseID = parseInt(ids[0]);
    let wordID = parseInt(ids[1]);

    var id = 0;
    for (let i = 0; i < phraseID; i++) {
        id += state.groundTruthAnswers[i].length
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

// e.g. taskID = 'state.task-3-3' means that the index of the phrase is 3, and the index of the word inside the phrase is 3
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

        var taskID = '#state.task-' + phraseIndex.toString() + '-' + wordIndex.toString();
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

                if (state.wrongAnswers.has(taskID)) state.wrongAnswers.delete(taskID);
                if (!state.correctAnswers.has(taskID)) {
                    state.correctAnswers.add(taskID);
                    classie.removeClass(element, 'border-bottom-danger');
                    classie.addClass(element, 'border-bottom-success');
                    animateCSS(element, 'fadeIn');
                    const wordID = getFlatIndexByID(taskID);
                    updateWordStatistics(state.globalStatisticsJSON, "correct",
                        state.statID, state.exerciseID, state.specificationID, wordID);
                }
            }
            // If the word is correct and is not empty -> set up red background
            else {
                if (state.correctAnswers.has(taskID)) state.correctAnswers.delete(taskID);
                if (userAnswer !== '') {
                    if (!state.wrongAnswers.has(taskID)) {
                        state.wrongAnswers.add(taskID);
                        classie.removeClass(element, 'border-bottom-success');
                        classie.addClass(element, 'border-bottom-danger');
                        animateCSS(element, 'fadeIn');
                    }
                    const wordID = getFlatIndexByID(taskID);
                    updateWordStatistics(state.globalStatisticsJSON, "wrong",
                        state.statID, state.exerciseID, state.specificationID, wordID);
                    // console.log('Update word stat');
                    // console.log(state.globalStatisticsJSON);
                }
            }
            // Next ID
            wordIndex += 1;
            taskID = '#state.task-' + phraseIndex.toString() + '-' + wordIndex.toString();
        }
    }
    // Save statistics
    localStorage.setItem('state.globalStatisticsJSON', JSON.stringify(state.globalStatisticsJSON));

    // console.log('Correct: ');
    // printSet(state.correctAnswers);
    // console.log('Wrong: ');
    // printSet(state.wrongAnswers);
}

function initializeInputHandlers() {
    // Handle pressing the enter key
    var inputs = $(':input').keyup(function (e) {
        if (e.which === 13) {
           // e.preventDefault();
            let nextInput = inputs.get(inputs.index(this) + 1);
            if (nextInput) {
                // If the next element is an INPUT -> switch to the next input.
                if (nextInput.tagName === 'INPUT') {
                    nextInput.focus();
                }
                // If the next element is the Button -> check the state.task by emulating the button click.
                else {
                    let nextID = '#' + $(nextInput).attr('id');
                    $(nextID).click();

                    // If there is the next state.task -> go to it
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
                    state.correctAnswers.delete(taskID);
                    classie.removeClass(element, 'border-bottom-success');
                }
                if (isIncorrect) {
                    state.wrongAnswers.delete(taskID);
                    classie.removeClass(element, 'border-bottom-danger');
                }
                animateCSS(element, 'fadeIn');
            }
        }
    });

    // Get the button and check all related words inside the state.task
    $('.btn-check-state.task').on('click', function () {
        checkFullTask(this);
    });

    // Check all exercises
    $('.btn-check-all').on('click', function () {
        $(".btn-check-state.task").each(function () {
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

                if ((taskType === state.task && taskSpecify === state.specifiedTask) && !state.requestFromOutside) return false;
                //  Update the state.task and only then reinitialize the globals
                updateTask(state.server+'/app/state.task', state.text, taskType, taskSpecify).then(function () {
                    updateGlobalParameters();
                    initializeInputHandlers();
                    initializeClassie();

                    const taskStr = idToString('#'+id);
                    changeElementContent('#tasksCardTitle', taskStr);
                }).catch(function (e) {
                    console.log(e);
                    // TODO: Update logic.
                    if (state.requestFromOutside) {
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
    if (state.requestFromOutside) {
        console.log('Request From Outside. ID =', state.requestFromOutside);
        $('#'+state.requestFromOutside).trigger('click');
        localStorage.setItem('state.requestFromOutside', '');
    } else {
        state.requestFromOutside = true;
        const id = '#TASK-'+state.task+'-'+state.specifiedTask;
        $(id).trigger('click');
        const taskStr = idToString(id);
        changeElementContent('#tasksCardTitle', taskStr);
    }
});
