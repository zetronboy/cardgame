from flask import (Flask, #installed with pip
	escape, #to html escape a string for the web
	url_for, #relative paths
	render_template, #for linking html files
	request, #for accessing the http req params
	redirect, #for getting back to root uri
	current_app, #for accessing app facory in __init__
	Blueprint #for plugin games
	)
from ... import socketio # instantiated in __init__.py and bound to app
from . import tcg

@tcg.route('/play', methods=['GET'])
def play():
	"""starts a game with specified player.
	Creates player and game objects,
	assigns to global players and games dicts
	client expected to connect to websocket using same room as game id"""
	player_id = request.remote_addr # who is asking to play
	opponent_id = request.args.get('opponent') # who they want to play
	game_type = request.args.get('game')
	if opponent_id in players:
		if game_type in supported_games_list:
			# create the game and mark the players assigned
			# they will connect to the game room with winsocket to play

			new_game = CardGame(player_id, opponent_id)
			gameid = new_game_id()
			players[player_id] = {'game': gameid}
			players[opponent_id] = {'game': gameid}
			games[gameid] = new_game
			
			#return str(json.dumps(players))
			URL = 'http://'+ gethostname() +':'+ str(listen_port) # we dont need this
			#TODO specify the music in the URL, maybe random
			update_lobby() #if client is told they are in a game they move to it
			return render_template('game.html', auto_refresh=False, room=gameid,  version=VERSION)
		else:
			return("could not find {} in supported game list".format(game_type))
	else:
		return("could not find {} in players".format(opponent_id))
