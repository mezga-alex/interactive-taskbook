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

$(document).ready(() => {
    $("input").on("keydown", function checkSingleAnswer(e) {
        if (e.keyCode == 13) {
            // Get phrase id and phrase word id
            let taskID = $(this).attr('id');
            let userAnswer = $(this).val();
            // Check if the answer is correct
            let isCorrect = checkAnswer(taskID, userAnswer);

            if (isCorrect) {
                alert('Correct');
            } else {
                alert('Peredelivai');
            }
        }
    });

    $('.btn-check-task').on('click', function checkMultipleAnswers(e) {
        let taskPhrasesIndices = $(this).attr('id').match(/\d+/g);
        for (let phraseIndex of taskPhrasesIndices) {
            var isCorrect = true;
            var wordIndex = 0;
            var taskID = '#task-' + phraseIndex.toString() + '-' + wordIndex.toString();
            while (isCorrect && ($(taskID).length !== 0)) {
                let userAnswer = $(taskID).val();
                isCorrect = checkAnswer(taskID, userAnswer);

                if (isCorrect) {
                    alert(taskID + ' Correct');
                } else {
                    alert(taskID + ' Peredelivai');
                }

                wordIndex += 1;
                taskID = '#task-' + phraseIndex.toString() + '-' + wordIndex.toString();
            }

        }

    });
});