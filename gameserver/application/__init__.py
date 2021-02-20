"""
application holds routes for connecting players to plugins
and gamemanager to instantiate and provision plugins
plugins plug into the application
plugins impliment a abstract interface to start/stop plugins
"""
from flask import Blueprint
from flask_socketio import SocketIO
from . import routes # __init__.py
from .gamemanager import GameManager
from .playermanager import PlayerManager
bp = Blueprint('application',
	__name__,
	url_prefix='/',
	template_folder='templates')

# to use these "from . import game_mgr, player_mgr"
game_mgr = GameManager()
player_mgr = PlayerManager()
