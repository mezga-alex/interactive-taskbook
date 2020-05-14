function backToTasks() {
    $('a').on('click', function isUpdateTask(e) {
        let id = $(this).attr('id');
        if (id && id !== 'build-chart-btn') {
            localStorage.setItem('requestFromOutside', id);
        }

    });
}

// Add canvas element
function addCanvas() {
    const canvasHTML = '<div class="chart-pie">' +
                       '<canvas id="myPieChart"></canvas>' +
                       '</div>' +
                       '<div class="mt-4 text-center small">' +
                       '<span class="mr-2">' +
                       '<i class="fas fa-circle text-success"></i> Correct</span>' +
                       '<span class="mr-2">' +
                       '<i class="fas fa-circle text-danger"></i> Wrong</span>' +
                       '</div>'

    $("#chart-body").empty();
    $("#chart-body").append(canvasHTML);
}

// Show the image if there is no results
function noResultsVisualization() {
    const text = "Hmm... It looks like you haven't completed tasks of this type yet."
    const html = '<img class="mx-auto d-block" style="width: 25rem; margin-top: 1rem; margin-bottom: 1rem;" ' +
                 'src="../img/undraw_screen_time_vkev.svg" alt="">' +
                  '<p class="mb-4 text-center">' + text + '</p>';

    $("#chart-body").empty();
    $("#chart-body").append(html);
}

// Count statistics with Wrong/Correct answers
function countAnswersStatistics(statisticsJSON, tasks, specifiedTasks) {
    if (tasks.size === 0)
        tasks = new Set(['PASSIVE_VOICE', 'ACTIVE_VOICE']);
    if (specifiedTasks.size === 0)
        specifiedTasks.add('ALL')

    var correctAnswers = 0;
    var wrongAnswers = 0;

    console.log(tasks, specifiedTasks)
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
function visualizeStatistics(statisticsJSON, tasks=new Set(), specifiedTask = new Set(), typeOfVisualization='pie', elementID="myPieChart") {
    try {
        switch (typeOfVisualization) {
            case 'pie':
                const dataValue = countAnswersStatistics(statisticsJSON, tasks, specifiedTask);
                console.log(dataValue);

                if ((dataValue[0] + dataValue[1]) !== 0) {
                    addCanvas();
                    createPieChart(dataValue);
                } else noResultsVisualization();
                break;
            default:
                console.log('ERROR PLOTTING');
                noResultsVisualization();
                break;
        }
    }
    catch(e) {
        noResultsVisualization();
        console.log(e);
    }
}

// Take parameters from the selector
function getChartParameters() {
    var tasks = new Set();
    var specifiedTasks = new Set();
    var selectorSet = new Set($("#tasksSelector").val());
    if (selectorSet.has("ACTIVE_VOICE")) {
        tasks.add("ACTIVE_VOICE");
        selectorSet.delete("ACTIVE_VOICE");
    }
    if (selectorSet.has("PASSIVE_VOICE")) {
        tasks.add("PASSIVE_VOICE");
        selectorSet.delete("PASSIVE_VOICE");
    }
    specifiedTask = selectorSet;

    console.log('Tasks: ', tasks, tasks.size);
    console.log('SpecifiedTasks: ', specifiedTask, specifiedTask.size);
    return [tasks, specifiedTask];
}

// Handle build-button click
function buildChartButtonControl() {
    $("#build-chart-btn").on("click", () => {
        var globalStatisticsJSON = JSON.parse(localStorage.getItem("globalStatisticsJSON"));
        if (!globalStatisticsJSON) {
            getDataBaseJSON(server+'/get_data', extensionID).then(function(value) {
                        console.log(value,': Response received');
                        globalStatisticsJSON = JSON.parse(localStorage.getItem("globalStatisticsJSON"));
                        const parameters = getChartParameters();
                        const tasks = parameters[0];
                        const specifiedTasks = parameters[1];

                        visualizeStatistics(globalStatisticsJSON, tasks, specifiedTasks)
                    }, function(reason) {
                        console.log(reason, ': No results');

                        // Simulate error
                        visualizeStatistics(null, null, null);
                    });
        } else {
            const parameters = getChartParameters();
            const tasks = parameters[0];
            const specifiedTasks = parameters[1];

            visualizeStatistics(globalStatisticsJSON, tasks, specifiedTasks)
        }
    });
}

// Selector handler
function selectorControl() {
    $("#tasksSelector").change(function(){
        const tasksSet = new Set($("#tasksSelector").val());
        console.log(tasksSet);
        if (tasksSet.has('ACTIVE_VOICE') || tasksSet.has('PASSIVE_VOICE')) {
            $( "#specifiedTasks" ).prop( "disabled", false );
            $( ".both-types" ).removeClass("text-gray-600").addClass("text-gray-900");;

            if (tasksSet.has('PASSIVE_VOICE')) {
                $( ".passive-only" ).prop( "disabled", false );
                $( ".passive-only" ).removeClass("text-gray-600").addClass("text-gray-900")
            } else {
                $( ".passive-only" ).prop( "disabled", true );
                $( ".passive-only" ).removeClass("text-gray-900").addClass("text-gray-600");
            }
            $("#tasksSelector").selectpicker("refresh");

        } else {
            $( "#specifiedTasks" ).prop( "disabled", true );
            $( ".both-types" ).removeClass("text-gray-900").addClass("text-gray-600");
            $( ".passive-only" ).removeClass("text-gray-900").addClass("text-gray-600");
            $("#tasksSelector").selectpicker("refresh");
        }
    })
}

// Initialize control handlers
function handleControlElements() {
    backToTasks();
    selectorControl();
    buildChartButtonControl();
}

$(document).ready(() => {
    handleControlElements();
    $("#build-chart-btn").trigger("click");
});