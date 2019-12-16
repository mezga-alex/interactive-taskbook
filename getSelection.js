var sel = ""
chrome.tabs.executeScript({
    code: "window.getSelection().toString();"
}, function(selection) {
    sel = selection[0]
});

var btnFind = document.querySelector('#btn-find');
btnFind.addEventListener('click', function() {
    if (sel.length) {
        chrome.extension.sendMessage({ 'data': [task, sel] }, function(response) {

        })
    }
})