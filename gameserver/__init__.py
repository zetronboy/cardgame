from flask import Flask 
from flask_socketio import SocketIO

socketio = SocketIO()

# add more games here

def create_app():
	_app = Flask(__name__)
	_app.config['SECRET_KEY']='89b256e523423423f9c499dbf83' #for wtf_forms
	socketio.init_app(_app, always_connect=True, async_mode='threading')

	from .lobby import app as lobby
	_app.register_blueprint(lobby)
	from .games.tcg import tcg
	_app.register_blueprint(tcg)
	# add more games here

	return _app