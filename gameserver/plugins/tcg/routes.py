from flask import (  #installed with pip
	#to html escape a string for the web
	#relative paths
	render_template, #for linking html files
	request, #for accessing the http req params
	#for getting back to root uri
	#for accessing app facory in __init__
	Blueprint #for plugin plugins
	)
from gameserver.application.gamemanager import GameManager #game collection
from .. import socketio
bp = Blueprint('tcg', __name__, url_prefix='/tcg') #tradding card game


@bp.route('/play', methods=['GET'])

