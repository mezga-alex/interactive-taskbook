function noResultsVisualization() {
    const text = "Hmm... It looks like you haven't completed tasks of this type yet."
    const html = '<img class="mx-auto d-block" style="width: 25rem; margin-top: 1rem; margin-bottom: 1rem;" ' +
                 'src="../img/undraw_screen_time_vkev.svg" alt="">' +
                  '<p class="mb-4 text-center">' + text + '</p>';

    $("#chart-body").empty()
    $("#chart-body").append(html);
}

// Count statistics with Wrong/Correct answers
function countAnswersStatistics(statisticsJSON, tasks, specifiedTasks) {
    if (tasks = 'ALL')
        tasks = new Set(['PASSIVE_VOICE', 'ACTIVE_VOICE']);
    else tasks = new Set([tasks]);

    if (!Array.isArray(specifiedTasks))
        specifiedTasks = [specifiedTasks];

    specifiedTasks = new Set(specifiedTasks);

    var correctAnswers = 0;
    var wrongAnswers = 0;

    for (const articleStatistics of statisticsJSON.statistics) {
        for (const exercise of articleStatistics.exercises) {
            if (tasks.has(exercise.task)) {
                for (const specification of exercise.specifications) {
                    if (specifiedTasks.has(specification.specifiedTask) || specifiedTasks.has('ALL')) {
                        for (const word of specification.words) {
                            correctAnswers += word.correct;
                            wrongAnswers += word.wrong;
                        }
                    }
                }
            }
        }
    }
    return [wrongAnswers, correctAnswers];
}

// Main plotting function
// TODO: Add another Charts
function visualizeStatistics(statisticsJSON, tasks='ALL', specifiedTask = 'ALL', typeOfVisualization='pie', elementID="myPieChart") {
    try {
        switch (typeOfVisualization) {
            case 'pie':
                const dataValue = countAnswersStatistics(statisticsJSON, tasks, specifiedTask);
                createPieChart(dataValue);
                break;
            default:
                console.log('ERROR PLOTTING');
                break;
        }
    }
    catch(e) {
        noResultsVisualization();
//         alert("Hmm... It looks like you haven't completed tasks of this type yet.");
        console.log(e);
    }
}

$(document).ready(() => {
    const globalStatisticsJSON = JSON.parse(localStorage.getItem("globalStatisticsJSON"));
    visualizeStatistics(globalStatisticsJSON)
});