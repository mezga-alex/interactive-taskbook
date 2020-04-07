function output_pos(pos){
  var posWords = JSON.parse(localStorage.getItem("pos_words"));
  // For future logic
  var posIndices = JSON.parse(localStorage.getItem("pos_indices"));

  if (posWords !== null && posWords.length > 0) {
      let setOfWords = new Set(posWords);
      let count = 1;
      // same as: for(let value of set)
      for(let word of setOfWords) {
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


function output_exercise(phrases, phrases_indices, phrases_lexemes, phrases_sents){

    if (phrases !== null && phrases.length > 0) {
        // FIRST phrase appending
        let phrases_space = "1) " + phrases[0].join(" ").toUpperCase();
        let para = document.createElement("p");
        let node = document.createTextNode(phrases_space);
        para.appendChild(node);
        let element = document.getElementById("put_passive");
        if (element !== null)
            element.appendChild(para);


        // ANOTHER phrases appending
        for(var i = 1; i < phrases.length; i++){
            let phrases_space = phrases[i].join(" ").toUpperCase();
            if (phrases_sents[i] !== phrases_sents[i-1]) {
                phrases_space = (i+1).toString() + ") " + phrases_space;
                //bkg.console.log(phrases_space);
            }
            let para = document.createElement("p");
            let node = document.createTextNode(phrases_space);
            para.appendChild(node);
            let element = document.getElementById("put_passive");
            if (element !== null)
                element.appendChild(para);
        }


        // ANOTHER sentences appending
        var phrases_sent_proc;
        var count = 0;
        var is_similar = false;
        for(var i = 0; i < phrases_sents.length; i++) {
            if (!is_similar) {
                phrases_sent_proc = phrases_sents[i];
            }
            count += 1;

            for (var j = 0; j < phrases_indices[i].length; j++) {
                let left_index = phrases_indices[i][j][0];
                let right_index = phrases_indices[i][j][1];
                let substr = phrases_sent_proc.substring(left_index, right_index);

                phrases_sent_proc = phrases_sent_proc.substring(0, left_index) + "_".repeat(substr.length)
                    + phrases_sent_proc.substring(right_index, phrases_sent_proc.length);

            }

            let phrases_lexeme_build = "( " + phrases_lexemes[i].join(", ") + " )";
            if ((phrases_sents[i] !== phrases_sents[i+1]) || (i === phrases_sents.length)) {
                // console.log(phrases_sent_proc);
                para = document.createElement("p");
                node = document.createTextNode((count).toString() + ") " + phrases_sent_proc + '\n' + phrases_lexeme_build );
                para.appendChild(node);
                element = document.getElementById("put_text");
                if (element !== null)
                    element.appendChild(para);
                    var x = document.createElement("INPUT");
                    x.setAttribute("type", "text");
                    x.setAttribute("id", "input"+(i+1).toString());
                    x.setAttribute("value", "Enter your answer");
                    element.appendChild(x);
                is_similar = false;
            } else {
                is_similar = true;
            }
            // bkg.console.log(phrases_sent_proc);
        }
    }
}


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

var color;
$('.btn-color').on('click', () => {
  color = $(this).attr('data-color');
})

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

  var speech = $('#speech').val();
  var tense = $('#tense').val();
  var passive_voice = $('#passive_voice').val();

   // bkg.console.log(speech + "|" + tense + "|" + passive_voice + "|" + color);

  chrome.tabs.getSelected(null, (tab) => {
        var tabId = tab.id;
        var tabUrl = tab.url;
        var text = "";
        PARSE_UTILS.keywordInterval(tabUrl, (text) => {
            data = JSON.stringify({
                "text": text,
                "pos": speech,
                "tense": tense,
                "passive_voice": passive_voice,
                "color": color
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
                  'Access-Control-Allow-Origin':'*',
                  "content-type": "application/json"
                })
            })
            .then( (response) => {
              if (response.status != 200) {
                console.log(`Looks like there was a problem. Status code: ${response.status}`);
                return null;
              }

              response.json().then( (data) => {
                  let pos_result = data["pos_result"];
                  let active_result = data["active_result"];
                  let passive_result = data["passive_result"];
                  var is_pos = false;
                  var is_active = false;
                  var is_passive = false;

                  if (pos_result != "") {
                    //bkg.console.log(speech);
                      is_pos = true;
                      localStorage.setItem('pos_words', JSON.stringify(pos_result[0]));
                      localStorage.setItem('pos_indices', JSON.stringify(pos_result[1]));
                      if (speech == "all")
                          localStorage.setItem('pos_tags', JSON.stringify(pos_result[2]));
                  }

                  if (active_result != "") {
                      is_active = true;
                      localStorage.setItem('active_phrases', JSON.stringify(active_result[0]));
                      localStorage.setItem('active_phrases_indices', JSON.stringify(active_result[1]));
                      localStorage.setItem('active_phrases_lexemes', JSON.stringify(active_result[2]));
                      localStorage.setItem('active_phrases_sents', JSON.stringify(active_result[3]));
                  }

                  if (passive_result != "") {
                      is_passive = true;
                      localStorage.setItem('passive_phrases', JSON.stringify(passive_result[0]));
                      localStorage.setItem('passive_phrases_indices', JSON.stringify(passive_result[1]));
                      localStorage.setItem('passive_phrases_lexemes', JSON.stringify(passive_result[2]));
                      localStorage.setItem('passive_phrases_sents', JSON.stringify(passive_result[3]));
                  } 
       
                  localStorage.setItem('is_pos', JSON.stringify(is_pos));
                  localStorage.setItem('is_active', JSON.stringify(is_active));
                  localStorage.setItem('is_passive', JSON.stringify(is_passive));

                  chrome.tabs.create({'url': './openPage/result.html' }, (tab) => {});
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
        output_exercise(active_phrases, active_phrases_indices, active_phrases_lexemes, active_phrases_sents);
    }

    if (is_passive){
        var passive_phrases = JSON.parse(localStorage.getItem("passive_phrases"));
        var passive_phrases_indices = JSON.parse(localStorage.getItem("passive_phrases_indices"));
        var passive_phrases_lexemes = JSON.parse(localStorage.getItem("passive_phrases_lexemes"));
        var passive_phrases_sents = JSON.parse(localStorage.getItem("passive_phrases_sents"));
        output_exercise(passive_phrases, passive_phrases_indices, passive_phrases_lexemes, passive_phrases_sents);
    }

    if (is_pos){
        output_pos();
    }
});
