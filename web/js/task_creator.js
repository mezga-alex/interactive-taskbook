let collapseCardStartId1HTML = '<!-- Collapsable Card Example -->' +
    '<div class="card shadow mb-4">' +
    '<a href="#';
// -> Insert ID
let collapseCardEndId1StartId2HTML = '" class="d-block card-header py-3" data-toggle="collapse" ' +
    'role="button" aria-expanded="true" aria-controls="';
// -> Insert ID again
let collapseCardEndId2StartHeaderHTML = '">' + '<h6 class="m-0 font-weight-bold text-primary">';
// -> Insert Header
let collapseCardEndHeaderStartId3HTML = '</h6>' + '</a>' + '<!-- Card Content - Collapse -->' + '<div class="collapse show" id="';
// -> Insert ID again
let collapseCardEndId3StartTaskHTML = '">' + '<div class="card-body">';
// -> Insert task
let collapseCardEndTaskHTML = '</div></div></div>';


function newTaskRequest(server, text, task, specifiedTask) {
    return new Promise((resolve, reject) => {
        let data = JSON.stringify({
            "text": text,
            "task": task,
            "specifiedTask": specifiedTask
        });

        fetch(server, {
            method: "POST",
            credentials: "include",
            body: data,
            cache: "no-cache",
            headers: new Headers({
                'Access-Control-Allow-Origin': '*',
                "content-type": "application/json"
            })
        }).then((response) => {
            if (response.status !== 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                reject("Error");
            }

            response.json().then((data) => {
                let result = data["result"];
                if (result[0].length !== 0) {
                    localStorage.setItem('text', text);
                    localStorage.setItem('task', task);
                    localStorage.setItem('specifiedTask', specifiedTask);
                    localStorage.setItem('result', JSON.stringify(result));

                    resolve("Success");
                }
                else reject("No matches")
            });
        }).catch(function (error) {
            console.log("Fetch error: " + error);
            reject("Error")
        });
    })
}

function createTaskByResult(task, result) {
    if (task === 'POS') {
        let posWords = result[0];
        let posIndices = result[1];

        outputPos(posWords, posIndices);
    }

    if (task === 'ACTIVE_VOICE') {
        let activePhrases = result[0];
        let activePhrasesIndices = result[1];
        let activePhrasesLexemes = result[2];
        let activePhrasesSents = result[3];

        outputExercise(activePhrases, activePhrasesLexemes, activePhrasesIndices, activePhrasesSents);
    }

    if (task === 'PASSIVE_VOICE') {
        let passivePhrases = result[0];
        let passivePhrasesIndices = result[1];
        let passivePhrasesLexemes = result[2];
        let passivePhrasesSents = result[3];

        outputExercise(passivePhrases, passivePhrasesLexemes, passivePhrasesIndices, passivePhrasesSents);
    }
    resizeInputs();
}

function getResultAttribute(result, task, attr) {
    switch (task) {
        case 'POS':
            switch (attr) {
                case 'words':
                    return result[0];
                case 'indices':
                    return result[1];
                default:
                    return null
            }
        case 'ACTIVE_VOICE':
        case 'PASSIVE_VOICE':
            switch (attr) {
                case 'phrases':
                    return result[0];
                case 'indices':
                    return result[1];
                case 'lexemes':
                    return result[2];
                case 'sentences':
                    return result[3];
                default:
                    return null;
            }
        default:
            return null;
    }
}

function updateTask(server, text, task, specifiedTask) {
    return new Promise((resolve, reject) => {
        // Delete ccurrent content
        // TODO: Save current results for statistics
        newTaskRequest(server, text, task, specifiedTask).then(function () {
            $("#put_text").empty();
            result = JSON.parse(localStorage.getItem("result"));
            createTaskByResult(task, result);
            resolve("Success");
        }).catch(function () {
            reject("No matches")
        });
    })
}

function collapseCardWrapper(taskID, task) {
    return collapseCardStartId1HTML + 'collapseCard-' + taskID + collapseCardEndId1StartId2HTML + 'collapseCard-' + taskID +
        collapseCardEndId2StartHeaderHTML + 'Task ' + taskID +
        collapseCardEndHeaderStartId3HTML + 'collapseCard-' + taskID + collapseCardEndId3StartTaskHTML + task + collapseCardEndTaskHTML;
}

function outputPos(posWords, posIndices) {
    if (posWords !== null && posWords.length > 0) {
        let setOfWords = new Set(posWords);
        let count = 1;
        // same as: for(let value of set)
        for (let word of setOfWords) {
            para = document.createElement("p");
            node = document.createTextNode((count).toString() + ") " + word.toUpperCase());
            para.appendChild(node);
            element = document.getElementById("put_text");
            if (element !== null)
                element.appendChild(para);
            count += 1;
        }
    }
}

function outputExercise(phrases, phrases_lexemes, phrases_indices, phrases_sents) {
    if (phrases !== null && phrases.length > 0) {
        var count = 1;
        var is_different = true;
        // Iterate over phrases
        for (var i = 0; i < phrases.length; i++) {
            // If the phrase is in a new sentence
            if (is_different) {
                var cur_sent = phrases_sents[i];
                var processed_sentence = '';
                // We need a button id related to all the correct phrases ids.
                // Example: if we have 2 phrases in the same sentence with their ids = 9, 10,
                // we create Button Id = 'task-9-10' and so on.
                var checkButton = '<div class="task-btn"><button class="btn-check-task", id="task-';
                var left_index = 0;
            }

            checkButton += i.toString();
            // Iterate over words in the phrase
            for (var j = 0; j < phrases[i].length; j++) {
                var right_index = phrases_indices[i][j][0];
                // We create intervals from the right side of the previous word to the left side of the next word:
                // Left Text index = Right Word index and Right Text index = Left Word index
                //
                // Create ID in this format:
                // id=task_i_j
                var input =

                    '<span class="input input--kaede align-middle" ' +
                    'id="span-task-' + i.toString() + '-' + j.toString() + '">\n' +
                    '<input class="input__field input__field--kaede" type="text" ' +
                    'id="task-' + i.toString() + '-' + j.toString() + '" />\n' +
                    '<label class="input__label input__label--kaede" for="task-' + i.toString() + '-' + j.toString() + '">\n' +
                    '<span class="input__label-content input__label-content--kaede">' + phrases_lexemes[i][j] + '</span>\n' +
                    '</label>\n' +
                    '</span>\n';

                processed_sentence += cur_sent.substring(left_index, right_index) + input;

                left_index = phrases_indices[i][j][1];
            }
            // If the next phrase is in another sentence - append created element to the page
            if ((i === phrases_sents.length - 1) || (phrases_sents[i] !== phrases_sents[i + 1])) {
                checkButton += '">Check answers</button></div>';
                // Full task HTML
                processed_sentence = '<div class="task-p"><p>' + processed_sentence +
                    cur_sent.substring(left_index, cur_sent.length) + '</p></div>' + checkButton + '<hr>';

                // Create completed HTML element with separated tasks
                let fullTaskHTML = collapseCardWrapper(count.toString(), processed_sentence);

                $("#put_text").append(processed_sentence);
                count += 1;
                is_different = true;
            } else {
                checkButton += '-';
                is_different = false;
            }

        }
        b = '<button class="btn-check-all", id="task-' + i.toString() +
            '">Check all answers</button>';
        $("#put_text").append(b);

    }
}
