
var PARSE_UTILS = {
    minBodyTailLength: function () {
        return 100;
    },
    /**
     * Удаляет все что находится за пределами <body> (если существует), а затем удаляет
     * все теги <script>
     * @param html
     * @returns {void | string}
     */
    getStrippedBody: function (html) {
        let body = html.match(/<body[^>]*>(?:([^]*)<\/body>([^]*)|([^]*))/i);
        if (body && body.length > 1) {
            if (body[2] && body[2].length > this.minBodyTailLength()) {
                body = body[1] + ' ' + body[2];
            } else if (body[1] === undefined) {
                body = body[3];
            } else {
                body = body[1];
            }
        } else {
            body = html;
        }

        return body.replace(/<script\b[^>]*(?:>[^]*?<\/script>|\/>)/ig, '<blink/>');
    },

    /**
     * Clean HTML Page
     *
     * @param html
     * @param callback
     * @returns {string}
     */
    cleanHtmlPage: function (html, callback) {
        // Transmit text to lowercase
        // html = html.toLowerCase();
        html = this.getStrippedBody(html);
        // Get rid of everything besides letters
        html = html.replace(/<(script|style|object|embed|applet)[^>]*>[^]*?<\/\1>/g, '');

        // Remove tags
        html = html.replace(/<[^>]*>/g, '');

        if (callback)
            callback(html);
        else
            return html;
    },

    keywordInterval: function(url, callback) {
        let body = "";
        $.ajax({
            type: 'get',
            accepts: {
                "*": "*/".concat("*"),
                text: "test/plain",
                html: "text/html",
                xml: "application/xml, text/xml",
                json: "application/json, text/javascript",
                mode: "cors",
                origin: ""
            },
            contents: {
                xml: /xml/,
                html: /html/,
                json: /json/
            },
            responseFields: {
                xml: "responseXML",
                text: "responseText",
                json: "responseJSON"
            },
            converters: {
                "* text": String,
                "text html": !0,
                "text json": jQuery.parseJSON,
                "text xml": jQuery.parseXML
            },
            flatOptions: {
                url: !0,
                context: !0
            },
            url: url,
            cache: false,
            success: (resp) => {
                String.prototype.replaceAll = function(search, replacement) {
                    var target = this;
                    return target.replace(new RegExp(search, 'g'), replacement);
                };


                var html = PARSE_UTILS.cleanHtmlPage(resp).replaceAll('&#x27', "'").replaceAll(";", "");
                callback(html);
            },
            error: (e) => {
            }
        });
    },
};

// TODO: Deprecate
var color;
$('.btn-color').on('click', () => {
  color = $(this).attr('data-color');
});

var server = "http://poltavsky.pythonanywhere.com/process";
$("#switch-id").click(function() {
    // this function will get executed every time the #switch-id element is clicked (or tab-spacebar changed)
    if($(this).is(":checked")) // "this" refers to the element that fired the event
    {
        server = 'http://127.0.0.1:5000/process';
        alert('Be sure to run your localhost to evaluate results: '+ server);
    }  else {
        server = "http://poltavsky.pythonanywhere.com/process";
//        alert ("Running on remote server: "+ server);

    }
});


$("#btn-find").on("click", () => {
    //////////////////////////////////////////////
    // TODO: Update for the new visualization
    let pos = $('#POS').val();
    let active_voice = $('#ACTIVE_VOICE').val();
    let passive_voice = $('#PASSIVE_VOICE').val();
    let task = '';
    let specifiedTask = '';

    if (pos !== 'NONE')  {
        task = 'POS';
        specifiedTask = speech;
    }
    if (active_voice !== 'NONE')  {
        task = 'ACTIVE_VOICE';
        specifiedTask = active_voice;
    }
    if (passive_voice !== 'NONE')  {
        task = 'PASSIVE_VOICE';
        specifiedTask = passive_voice;
    }
    alert(task, specifiedTask);
    //////////////////////////////////////////////
    chrome.tabs.getSelected(null, (tab) => {
        let tabUrl = tab.url;
        PARSE_UTILS.keywordInterval(tabUrl, (text) => {
            data = JSON.stringify({
                "text": text,
                "task": task,
                "specifiedTask": specifiedTask
            });
            // chrome.tabs.create({'url': './openPage/result.html' });
            // for local inference use:
            // http://poltavsky.pythonanywhere.com/process
            // http://127.0.0.1:5000/process
            // alert(server);
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
                    if (response.status != 200) {
                        console.log(`Looks like there was a problem. Status code: ${response.status}`);
                        return null;
                    }

                    response.json().then((data) => {
                        let result = data["result"];
                        let is_pos = false;
                        let is_active = false;
                        let is_passive = false;

                        if (task === 'POS') {
                            //bkg.console.log(speech);
                            is_pos = true;
                            localStorage.setItem('pos_words', JSON.stringify(result[0]));
                            localStorage.setItem('pos_indices', JSON.stringify(result[1]));
                            if (speech === "all")
                                localStorage.setItem('pos_tags', JSON.stringify(result[2]));
                        }

                        if (task === 'ACTIVE_VOICE') {
                            is_active = true;
                            localStorage.setItem('active_phrases', JSON.stringify(result[0]));
                            localStorage.setItem('active_phrases_indices', JSON.stringify(result[1]));
                            localStorage.setItem('active_phrases_lexemes', JSON.stringify(result[2]));
                            localStorage.setItem('active_phrases_sents', JSON.stringify(result[3]));
                        }

                        if (task === 'PASSIVE_VOICE') {
                            alert('Lalala');
                            is_passive = true;
                            localStorage.setItem('passive_phrases', JSON.stringify(result[0]));
                            localStorage.setItem('passive_phrases_indices', JSON.stringify(result[1]));
                            localStorage.setItem('passive_phrases_lexemes', JSON.stringify(result[2]));
                            localStorage.setItem('passive_phrases_sents', JSON.stringify(result[3]));
                        }

                        localStorage.setItem('is_pos', JSON.stringify(is_pos));
                        localStorage.setItem('is_active', JSON.stringify(is_active));
                        localStorage.setItem('is_passive', JSON.stringify(is_passive));

                        chrome.tabs.create({'url': './openPage/result.html'}, (tab) => {
                        });
                    });
                })
                .catch(function (error) {
                    console.log("Fetch error: " + error);
                });
        });
    });
});

$(document).ready(() => {
    var is_pos = JSON.parse(localStorage.getItem("is_pos"));
    var is_active = JSON.parse(localStorage.getItem("is_active"));
    var is_passive = JSON.parse(localStorage.getItem("is_passive"));

    if (is_active){
        var active_phrases = JSON.parse(localStorage.getItem("active_phrases"));
        var active_phrases_indices = JSON.parse(localStorage.getItem("active_phrases_indices"));
        var active_phrases_lexemes = JSON.parse(localStorage.getItem("active_phrases_lexemes"));
        var active_phrases_sents = JSON.parse(localStorage.getItem("active_phrases_sents"));
        output_exercise(active_phrases, active_phrases_lexemes, active_phrases_indices, active_phrases_sents);
        passAnswers(active_phrases);
    }

    if (is_passive){
        var passive_phrases = JSON.parse(localStorage.getItem("passive_phrases"));
        var passive_phrases_lexemes = JSON.parse(localStorage.getItem("passive_phrases_lexemes"));
        var passive_phrases_indices = JSON.parse(localStorage.getItem("passive_phrases_indices"));
        var passive_phrases_sents = JSON.parse(localStorage.getItem("passive_phrases_sents"));
        output_exercise(passive_phrases,passive_phrases_lexemes, passive_phrases_indices, passive_phrases_sents);
        passAnswers(passive_phrases);
    }

    if (is_pos){
        output_pos();
    }
});
