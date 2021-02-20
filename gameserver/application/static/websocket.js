
function connect() {
	socket = io();
	socket.on('message', (payload) => {
		console.log('message '+ payload);
		displayNotification(payload);
	});

	socket.on('term-data', (payload) => {
		displayNotification('term-data'+ new Uint8Array(payload));
	});
	socket.on('player-state', (payload) => {
	    displayNotification('player-state');
		if (updatePlayerState) {
		    console.log('calling updatePlayerState()')
			updatePlayerState(payload); // impliment this on the web page
		}
	})
	socket.on('game-state', (payload) => {
	    console.log('game-state');
		if (updateGameState) {
			updateGameState(payload); // impliment this on the web page
		}
	})
	socket.on('term-state', (payload) => {
	    displayNotification('term-state');

	})
	socket.on('connect', () => {
		displayNotification('websocket connected ');
		if (onConnected) {
		    onConnected(); //impliment in web page
		}
	});
	socket.on('disconnect', (reason) => {
		displayNotification('disconnected, '+ reason);
	});

	socket.on('term-request', (request) => {
		displayNotification('socket received term-request: ' + request);
	});


}