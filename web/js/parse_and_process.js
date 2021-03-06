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

    keywordInterval: function (url, callback) {
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
                String.prototype.replaceAll = function (search, replacement) {
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

// chrome.tabs.create({'url': './openPage/result.html' });
// remote server:
// http://87.117.25.190:8050/
// for local inference use:
// http://poltavsky.pythonanywhere.com/process
// http://127.0.0.1:8050/
var server = "http://87.117.25.190:8060";
$("#switch-id").click(function () {
    // this function will get executed every time the #switch-id element is clicked (or tab-spacebar changed)
    if ($(this).is(":checked")) // "this" refers to the element that fired the event
    {
        server = 'http://127.0.0.1:5000/';
        alert('Be sure to run your localhost to evaluate results: ' + server);
    } else {
        server = "http://87.117.25.190:8060";
    }
});


$("#btn-find").on("click", () => {
    $(this).unbind("mouseenter mouseleave");
    let task = $('#task').val();
    let specifiedTask = $('#specifiedTask').val();
    if (task !== 'NONE' && specifiedTask !== 'NONE') {
        try {
            chrome.tabs.getSelected(null, (tab) => {
                let tabUrl = tab.url;
                PARSE_UTILS.keywordInterval(tabUrl, (text) => {
                    const taskID = 'TASK-'+task+'-'+specifiedTask;
                    localStorage.setItem('text', text);
                    localStorage.setItem('server', server);
                    localStorage.setItem('url', tabUrl);
                    localStorage.setItem('requestFromOutside', taskID);

                    chrome.tabs.create({'url': './openPage/result.html'}, (tab) => {
                    });
                });
            });
        }
        catch (e) {
            console.log(e);
        }
    }
});
