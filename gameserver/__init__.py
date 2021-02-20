from flask import Flask 
from flask_socketio import SocketIO

#from pathlib import Path
import importlib
import os
#
# to use this app factory:
# pip3 import -r requirements.txt
# export FLASK_APP=gameserver/main.py
# flask run (from cardgame folder)
#
# https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/


#global file logger used by others in the project
from .logger import Logger, Level
log = Logger()

socketio = SocketIO()

#scan plugins dir and create available game_list
game_list = [] #plugins

print("running script from "+ os.getcwd())
print("indexing plugins")
game_folders = os.listdir(os.path.join('gameserver', 'plugins'))
for game_folder in game_folders:
	game_title = game_folder
	game_list.append(game_title)
	print(f"Plugging in {game_title}")

def create_app():
	_app = Flask(__name__)
	_app.config['SECRET_KEY']='89b256e523423423f9c499dbf83' #for wtf_forms
	#with _app.app_context():
	socketio.init_app(_app, always_connect=True, async_mode='threading')

	#from .application import bp as lobby
	#_app.register_blueprint(lobby)

	for g in game_list:
		game_mod = importlib.import_module(f".plugins.{g}", package='gameserver')
		_app.register_blueprint(game_mod.bp)
		print(f"Registered blueprint for game {g}")
	# add more plugins to the plugins folder, follow example of others as blueprint

	return _app

