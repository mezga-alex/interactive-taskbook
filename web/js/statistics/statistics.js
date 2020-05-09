// Count statistics with Wrong/Correct answers
function countAnswersStatistics(statisticsJSON, tasks, specifiedTask) {
    if (tasks = 'ALL')
        tasks = new Set(['PASSIVE_VOICE', 'ACTIVE_VOICE']);
    else tasks = new Set([tasks]);
    var correctAnswers = 0;
    var wrongAnswers = 0;

    for (const articleStatistics of statisticsJSON.statistics) {
        for (const exercise of articleStatistics.exercises) {
            if (tasks.has(exercise.task)) {
                for (const specification of exercise.specifications) {
                    if (specification.specifiedTask === specifiedTask || specifiedTask === 'ALL') {
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
        alert('Hm. Something happened to your stats. Reload the page.');
        console.log(e);
    }
}

$(document).ready(() => {
    const globalStatisticsJSON = JSON.parse(localStorage.getItem("globalStatisticsJSON"));
    visualizeStatistics(globalStatisticsJSON)
});