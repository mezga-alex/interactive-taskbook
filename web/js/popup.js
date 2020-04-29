var specificVal = {
    POS: [
        ["NONE", "specify the task"],

        ["NOUN", "noun"],
        ["PRON", "pronoun"],
        ["VERB", "verb"],
        ["ADJ", "adjective"],
        ["ADV", "adverb"],
        ["ADP", "preposition"],
        ["INTJ", "interjection"],
    ],
    ACTIVE_VOICE: [
        ["NONE", "specify the task"],

        ["PRESENT_SIMPLE", "present simple"],
        ["PRESENT_CONTINUOUS", "present continuous"],
        ["PRESENT_PERFECT", "present perfect"],

        ["PAST_SIMPLE", "past simple"],
        ["PAST_CONTINUOUS", "past continuous"],
        ["PAST_PERFECT", "past perfect"],

        ["FUTURE_SIMPLE", "future simple"],
        ["FUTURE_PERFECT", "future perfect"],
    ],
    PASSIVE_VOICE: [
        ["NONE", "specify the task"],
        ["ALL", "all"],

        ["PRESENT_SIMPLE", "present simple"],
        ["PRESENT_CONTINUOUS", "present continuous"],
        ["PRESENT_PERFECT", "present perfect"],

        ["PAST_SIMPLE", "past simple"],
        ["PAST_CONTINUOUS", "past continuous"],
        ["PAST_PERFECT", "past perfect"],
        ["FUTURE_SIMPLE", "future simple"],
        ["FUTURE_PERFECT", "future perfect"],

        ["FUTURE_IN_THE_PAST_SIMPLE", "future in the past simple"],
        ["FUTURE_IN_THE_PAST_PERFECT", "future in the past perfect"],
        ["MODALS", "passives with modals"],
    ],
    NONE: [
        ["NONE", "select value"],
    ]
};


$(document).ready(function(){
    var specifiedTask = document.querySelector("#specifiedTask");

    $("#task").change(function(){
        specifiedTask.innerHTML = "";
        var val = $(this).children("option:selected").val();
        if (val !== 'NONE' && val !== undefined) {
            $( "#specifiedTask" ).prop( "disabled", false );
            for (let i = 0; i < specificVal[val].length; i++) {
                var o = new Option(specificVal[val][i][1], specificVal[val][i][0], false);
                $(o).addClass('selectpicker-option');
                specifiedTask.add(o);
                o = new Option(specificVal[val][i][1], specificVal[val][i][0], false);

                $('#specifiedTask').selectpicker('refresh');
            }
        } else {
            $( "#specifiedTask" ).prop( "disabled", true );
            let o = new Option('specify the task', 'NONE', false);
            specifiedTask.add(o);

            $('#specifiedTask').selectpicker('refresh');
        }
    });

    // $("#specifiedTask").change(function() {
    //     alert(1);
    //     var val = $(this).children("option:selected").val();
    //     if (val !== 'NONE' && val !== undefined) {
    //         alert(2);
    //         let task = $('#task');
    //         task.removeClass("selectpicker-selected");
    //         task.addClass('correct');
    //         task.selectpicker('refresh');
    //
    //         let specifiedTask = $('#specifiedTask');
    //         task.removeClass("selectpicker-selected");
    //         specifiedTask.addClass('correct');
    //         specifiedTask.selectpicker('refresh');
    //     }
    // });
});
