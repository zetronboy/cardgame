VERSION="0.4"
from flask import (Flask, #installed with pip
	escape, #to html escape a string for the web
	url_for, #relative paths
	render_template, #for linking html files
	request, #for accessing the http req params
	redirect, #for getting back to root uri
	current_app, #for accessing app facory in __init__
	Blueprint #for plugin games
				   )
#import eventlet
from flask_socketio import SocketIO, emit, send, join_room, rooms, leave_room
# export FLASK_ENV=development
# export FLASK_APP=clientview.py
# t http://localhost:5000
# or
# export FLASK_APP=main_.py
# export FLASK_DEBUG=True
# python -m flask run --host=0.0.0.0 --port=80
# or
# python3 ./clientview.py

from socket import gethostname
import traceback # call traceback.format_exc() on exceptions
from ..log import *
import json #dump dumps load loads
from ..games.tcg.game import Game as CardGame
from .. import socketio # instantiated in __init__.py and bound to app
from . import app

players = {} # {'192.168.1.123': {'nick': 'joey', 'game': 1}}, {'localhost': {'nick': None}}
#TODO i need a way to clear out old players who are not connected.
games = {}
listen_port = 81
supported_games_list = ['tcg'] 

@app.route('/', methods=['GET'])
def root():
	"""list connected players to start a game. pass nick= to name yourself.
	everyone starts in the lobby and click a link to join another player in battle
	returns supported games list and info about the client to identify themselves
	the client will get a list of players and active games from the websocket
	"""
	player_id = request.remote_addr #ip or hostname
	nickname = request.args.get('nick', '')

	global players
	#if player_hostip in players: del players[player_hostip] # if they were marked against a ip before we clear them out.
	players[player_id] = {'nick': nickname, 'game': 'lobby', 'games': supported_games_list} # after they join a game this gets {'game': [gameid]}

	#not needed URL = 'http://' + gethostname() + ':' + str(listen_port)  # we dont need this
	update_lobby() #mighbe be a new player 
	return render_template('lobby.html',
						auto_refresh=False,
						games=supported_games_list,
						roomid='lobby',
						nick=nickname,
						player=player_id,
						version=VERSION)


@app.route('/json')
def get_json():
	return str(games)

@app.route('/log')
def get_log():
	content = ''
	with open(log.log_file_name, 'r') as f:
		content = f.readlines()
	return str('<br />'.join(content))

#------------------------------------
# socketio
#------------------------------------

def update_lobby():
	"""send an update to lobby members with players list
	called when someone accesses the web root"""
	#emit trys to turn the object into JSON and passes to web	
	socketio.emit('player-state', players, room='lobby')

def update_socket_clients(roomid):
	"""sends websocket update with games and players to room members"""
	if roomid in games: 
		socketio.emit('game-state', games[roomid].toJson(), room=roomid)
	socketio.emit('player-state', players, room=roomid)

@socketio.on('term-request') #  , namespace='/chat')
def handle_command(data):
	try:
		clientId = request.sid
		log.debug("handle_command({}) from client {}".format(data, clientId))

	except Exception as e:
		log.error("handle_command Exception {}".format(e))


@socketio.on('message')
def handle_message(message):
	try:
		log.debug('io message {}'.format(message))
		send('got {}'.format(message))
	except Exception as e:
		log.error("io.message Exception {}\n{trace}".format(e, trace=traceback.format_exc()))


@socketio.on('connect')
def handle_connect():
	try:
		log.debug('socket connect {}'.format(request.sid))
		send('hello {}'.format(request.sid))

	except Exception as e:
		log.error("io.connect Exception {}\n{trace}".format(e, trace=traceback.format_exc()))


@socketio.on('join')
def on_join(data):
	try:
		game_id = data['room']  # client sends emit('join', { room': [processId] })

		player_id = request.remote_addr  # who is asking to play
		# lobby is where they wait to match up
		# otherwise its the game id from games[] dict
		if game_id:
			join_room(game_id)  # the room will be the processId index to watch
			client_id = request.sid
			log.debug("on_join({}) from client {} player={}".format(game_id, client_id, player_id))
			send('welcome to {}'.format(game_id))
			if player_id in players: #show player in the room/lobby
				players[player_id]['game'] = game_id
			else:
				players[player_id] = {'game': game_id }

			emit('player-state', players) #emits to this user
			#log.debug('emitted player-state')
			
			update_socket_clients(game_id)
		else:
			send("Missing room, emit 'join', { room': [appidhere] } ")
		

	except Exception as e:
		log.error("on_join {}\n{trace}".format(e, trace=traceback.format_exc()))


@socketio.on('disconnect')
def handle_disconnect():
	clientId = request.sid  # unique id for the websocket user
	log.debug('socket disconnect client {}'.format(clientId))
	send('goodby {}'.format(clientId))


@socketio.on('leave')
def on_leave(data):
	client_id = request.sid  # unique id for the websocket user
	player_id = request.remote_addr  # who is asking to play
	game_id = data['room']
	log.debug("on_leave id={} roomid={} data={} player={}".format(client_id, game_id, data, player_id))
	leave_room(game_id)
	for p in players:
		if p['game'] == game_id:
			p['game'] = None
	update_socket_clients(game_id) # sends update to clients in the room to kick them back to lobby
	if game_id in games: games[game_id] = None # delete the game
	send('sending you back to the lobby')


last_game_id = 0
def new_game_id():
	global last_game_id
	last_game_id += 1
	return last_game_id

if __name__ == '__main__':
	#websocket wraps flask run
	log.startlogging()
	socketio.run(app, port=listen_port, debug=True, host='0.0.0.0')
