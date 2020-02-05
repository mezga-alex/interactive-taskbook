// const Mercury = require('@postlight/mercury-parser');

// //import Mercury from @postlight/mercury-parser
// var url = "https://www.nytimes.com/2019/12/13/business/liu-jingyao-interview-richard-liu.html";
// Mercury.parse(url).then(result => console.log(result));
//var bkg = chrome.extension.getBackgroundPage();
// var flag = false;

function output_pos(pos){
  var posWords = JSON.parse(localStorage.getItem("pos_words"));
  // For future work
  var posIndices = JSON.parse(localStorage.getItem("pos_indices"));
  // para = document.createElement("p");
  // node = document.createTextNode($('#speech').val());
  // para.appendChild(node);
  // element = document.getElementById("put_text");
  if (element !== null)
      element.appendChild(para);

  if (posWords !== null && posWords.length > 0) {
      let setOfWords = new Set(posWords);
      let count = 1;
      // то же, что: for(let value of set)
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


function output_passive_voice(){
  var passive_phrases = JSON.parse(localStorage.getItem("passive_phrases"));
  var passive_phrases_indexes = JSON.parse(localStorage.getItem("passive_phrases_indexes"));
  var passive_phrases_lexemes = JSON.parse(localStorage.getItem("passive_phrases_lexemes"));
  var passive_phrases_sents = JSON.parse(localStorage.getItem("passive_phrases_sents"));

    if (passive_phrases !== null && passive_phrases.length > 0) {
        // FIRST phrase appending
        let passive_phrases_space = "1) " + passive_phrases[0].join(" ").toUpperCase();
        let para = document.createElement("p");
        let node = document.createTextNode(passive_phrases_space);
        para.appendChild(node);
        let element = document.getElementById("put_passive");
        if (element !== null)
            element.appendChild(para);

        // ANOTHER phrases appending
        for(var i = 1; i < passive_phrases.length; i++){
            let passive_phrases_space = passive_phrases[i].join(" ").toUpperCase();
            if (passive_phrases_sents[i] !== passive_phrases_sents[i-1]) {
                passive_phrases_space = (i+1).toString() + ") " + passive_phrases_space;
                //bkg.console.log(passive_phrases_space);
            }
            let para = document.createElement("p");
            let node = document.createTextNode(passive_phrases_space);
            para.appendChild(node);
            let element = document.getElementById("put_passive");
            if (element !== null)
                element.appendChild(para);
        }


        // ANOTHER sentences appending
        var passive_phrases_sent_proc;
        var coun = 0;
        var is_similar = false;
        for(var i = 0; i < passive_phrases_sents.length; i++) {
            if (!is_similar) {
                passive_phrases_sent_proc = passive_phrases_sents[i];
            }
            coun += 1;

            for (var j = 0; j < passive_phrases_indexes[i].length; j++) {
                let left_index = passive_phrases_indexes[i][j][0];
                let right_index = passive_phrases_indexes[i][j][1];
                let substr = passive_phrases_sent_proc.substring(left_index, right_index);

                passive_phrases_sent_proc = passive_phrases_sent_proc.substring(0, left_index) + "_".repeat(substr.length)
                    + passive_phrases_sent_proc.substring(right_index, passive_phrases_sent_proc.length);

            }

            let passive_phrases_lexeme_build = "( " + passive_phrases_lexemes[i].join(", ") + " )";
            if ((passive_phrases_sents[i] !== passive_phrases_sents[i+1]) || (i === passive_phrases_sents.length)) {
                // console.log(passive_phrases_sent_proc);
                para = document.createElement("p");
                node = document.createTextNode((coun).toString() + ") " + passive_phrases_sent_proc + '\n' + passive_phrases_lexeme_build );
                para.appendChild(node);
                element = document.getElementById("put_text");
                if (element !== null)
                    element.appendChild(para);
                is_similar = false;
            } else {
                is_similar = true;
            }
            // bkg.console.log(passive_phrases_sent_proc);
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
   * Чистим Html страницу.
   *
   * @param html
   * @param callback
   * @returns {string}
   */
  cleanHtmlPage: function (html, callback) {
      // Переводим все в нижний регистр
      // html = html.toLowerCase();
      // Выполняем описанную ранее функцию
      html = this.getStrippedBody(html);
      // Удаляем все, кроме текста
      html = html.replace(/<(script|style|object|embed|applet)[^>]*>[^]*?<\/\1>/g, '');
     
      // Удаляем теги
      html = html.replace(/<[^>]*>/g, '');
    
      if (callback)
          callback(html);
      else
          return html;
  },

  c1: function(text, result) {
    var para = document.createElement("p");
    var node = document.createTextNode("This is new.");
    para.appendChild(node);
    
    var element = document.getElementById("div1");
    element.appendChild(para);
  
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

$('#color_choice').on('click', () => {
  color = $(this).attr('data-color');
})




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
            fetch("http://127.0.0.1:5000/process", {
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
                  let passive_result = data["passive_result"];
                  var exercise_mode = 0; 
                  
                  if (pos_result != "") {
                    //bkg.console.log(speech);
                    exercise_mode += 1;
                    localStorage.setItem('pos_words', JSON.stringify(pos_result[0]));
                    localStorage.setItem('pos_indices', JSON.stringify(pos_result[1]));
                    if (speech == "all")
                      localStorage.setItem('pos_tags', JSON.stringify(pos_result[2]));
                  } 

                  if (passive_result != "") {
                    exercise_mode += 2;
                    localStorage.setItem('passive_phrases', JSON.stringify(passive_result[0]));
                    localStorage.setItem('passive_phrases_indexes', JSON.stringify(passive_result[1]));
                    localStorage.setItem('passive_phrases_lexemes', JSON.stringify(passive_result[2]));
                    localStorage.setItem('passive_phrases_sents', JSON.stringify(passive_result[3]));
                  } 
       
                  localStorage.setItem('exercise_mode', JSON.stringify(exercise_mode));
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
    var exercise_mode = JSON.parse(localStorage.getItem("exercise_mode"));

    if (exercise_mode == 1){
      output_pos();
    }

    if (exercise_mode == 2){
      output_passive_voice();
    }

    if (exercise_mode == 3){
      output_passive_voice();
      output_pos();
    }  
});
