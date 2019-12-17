var url = "https://www.nytimes.com/2019/12/11/climate/nyt-climate-newsletter-food-waste.html";

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
  success: function(resp) {
  	String.prototype.replaceAll = function(search, replacement) {
      var target = this;
      return target.replace(new RegExp(search, 'g'), replacement);
    };


    var dom = MONITOR_BACKGROUND_UTILS.cleanHtmlPage(resp).replaceAll('&#x27', "'").replaceAll(";", "");
    var kw = MONITOR_BACKGROUND_UTILS.cleanHtmlPage(keyword).replaceAll('&#x27', "'").replaceAll(";", "");


    if (!!(dom.indexOf(kw) + 1)) {
      console.log('No changes!');
        
    } else {
      jobs[k].dom_old = dom;
      chrome.storage.local.set({"MonitorJobs": jobs});


      CHROME_UTILS.sendNotification('Changes detected', 'url – ' + url + ', block', sound);
      console.log('Changes detected');
    }
  },
  error: function(resp) {
    console.log(resp);
  }
});
