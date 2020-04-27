// customization of select element
// var x, i, j, selElmnt, a, b, c;
// /*look for any elements with the class "custom-select":*/
// x = document.getElementsByClassName("custom-select");
// for (i = 0; i < x.length; i++) {
//     selElmnt = x[i].getElementsByTagName("select")[0];
//     /*for each element, create a new DIV that will act as the selected item:*/
//     a = document.createElement("DIV");
//     a.setAttribute("class", "select-selected");
//     a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
//     x[i].appendChild(a);
//     /*for each element, create a new DIV that will contain the option list:*/
//     b = document.createElement("DIV");
//     b.setAttribute("class", "select-items select-hide");
//     for (j = 1; j < selElmnt.length; j++) {
//         /*for each option in the original select element,
//         create a new DIV that will act as an option item:*/
//         c = document.createElement("DIV");
//         c.innerHTML = selElmnt.options[j].innerHTML;
//         c.addEventListener("click", function(e) {
//             /*when an item is clicked, update the original select box,
//             and the selected item:*/
//             var y, i, k, s, h;
//             s = this.parentNode.parentNode.getElementsByTagName("select")[0];
//             h = this.parentNode.previousSibling;
//             for (i = 0; i < s.length; i++) {
//                 if (s.options[i].innerHTML == this.innerHTML) {
//                     s.selectedIndex = i;
//                     h.innerHTML = this.innerHTML;
//                     y = this.parentNode.getElementsByClassName("same-as-selected");
//                     for (k = 0; k < y.length; k++) {
//                         y[k].removeAttribute("class");
//                     }
//                     this.setAttribute("class", "same-as-selected");
//                     break;
//                 }
//             }
//             h.click();
//         });
//         b.appendChild(c);
//     }
//     x[i].appendChild(b);
//     a.addEventListener("click", function(e) {
//         /*when the select box is clicked, close any other select boxes,
//         and open/close the current select box:*/
//         e.stopPropagation();
//         closeAllSelect(this);
//         this.nextSibling.classList.toggle("select-hide");
//         this.classList.toggle("select-arrow-active");
//     });
// }

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

// var taskType = document.querySelector("#taskType");
var specifiedTask = document.querySelector("#specifiedTask");
// window.onload = selectParams;

$(document).ready(function(){
    $("#task").change(function(){
        // alert("The text has been changed.");
        specifiedTask.innerHTML = "";
        var c = $(this).children("option:selected").val();
        // alert("You have selected - " + c);
        if (c !== 'NONE' & c !== undefined) {
            document.getElementById("specifiedTask").disabled = false;
            for (let i = 0; i < specificVal[c].length; i++) {
                o = new Option(specificVal[c][i][1], specificVal[c][i][0], false);
                specifiedTask.add(o);
            }
        } else {
            document.getElementById("specifiedTask").disabled = true;
            o = new Option('specify the task', 'NONE', false);
            specifiedTask.add(o);
        }
    });
});

