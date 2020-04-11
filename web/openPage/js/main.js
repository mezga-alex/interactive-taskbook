let answers;
var strictCheck = false;

function passAnswers(newAnswers) {
    answers = newAnswers;
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
            var element = document.getElementById(taskID.substr(1));
            // If the word is correct -> set up green background
            if (isCorrect) {
                classie.removeClass(element, 'input__field--kaede-incorrect');
                classie.addClass(element, 'input__field--kaede-correct');

             // If the word is correct and is not empty -> set up red background
            } else if (userAnswer !== '') {
                classie.removeClass(element, 'input__field--kaede-correct');
                classie.addClass(element, 'input__field--kaede-incorrect');
            }

            // Next ID
            wordIndex += 1;
            taskID = '#task-' + phraseIndex.toString() + '-' + wordIndex.toString();
        }
    }
}

$(document).ready(() => {
    // Handle pressing the enter key
    var inputs = $(':input').keypress(function(e){
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
        }
    });

    // Get the button and check all related words inside the task
    $('.btn-check-task').on('click', function checkMultipleAnswers(e) {
        checkFullTask(this);
    });
});