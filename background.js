chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
    $.ajax({
        url: 'http://localhost/',
        dataType: 'json',
        async: true,
        data: { textTask: request.data[0], textString: request.data[1] },
        success: function(resp) {
            chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
                for (var i = 0; i < tabs.length; i++) {
                    var currentTab = tabs[i].id;
                    chrome.tabs.executeScript(tabs[i].id, {
                        file: 'modal.js'
                    }, function() {
                        chrome.tabs.sendMessage(currentTab, { 'data': resp });
                    });
                }
            });
        }
    });
    sendResponse("");
    return true;

});