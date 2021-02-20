function displayNotification(messageString) {
	console.log(messageString);
	try{
		var dtStamp = new Date().toLocaleTimeString();
        messagesElm = document.getElementById('messages');
        if (messagesElm) {
            previous = messagesElm.innerHTML;
	    	messagesElm.innerHTML = dtStamp +': '+ messageString +"<br />"+ previous;
	    }
	} catch { console.log('error displayNotification in logevents.js finding messages element for notifications'); }
}