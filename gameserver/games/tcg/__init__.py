from flask import Blueprint 
tcg = Blueprint('tcg', __name__, url_prefix='/tcg') #tradding card game
from . import game, assets, player, routes