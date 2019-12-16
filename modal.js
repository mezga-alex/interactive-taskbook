chrome.runtime.onMessage.addListener(appendModal);

function appendModal(message) {
    var divModal = document.createElement('div');
    var spanClose = document.createElement('span');
    var divModalContent = document.createElement('div');
    var pText = document.createElement('p');
    var pLabel = document.createElement('p');
    divModal.style = "display:block;position:fixed;z-index:10;padding-top:100px;left:0;top:0;width:100%;height:100%;overflow:auto;background-color:rgb(0,0,0);background-color:rgba(0,0,0,0.4);";
    divModalContent.style = "background-color: #fefefe;margin: auto;padding: 20px;border: 1px solid #888;width: 80%;";
    spanClose.style = "color: #aaaaaa;float: right;font-size: 28px;font-weight: bold;cursor: pointer;";
    pText.innerText = message.data[1].text;
    pLabel.innerText = message.data[0].text;
    spanClose.innerHTML = "&times;";
    divModalContent.appendChild(spanClose);
    divModalContent.appendChild(pLabel);
    divModalContent.appendChild(pText);
    divModal.appendChild(divModalContent);
    spanClose.addEventListener('click', function() {
        document.body.removeChild(divModal);
    });
    document.body.appendChild(divModal);
    chrome.runtime.onMessage.removeListener(appendModal);
}