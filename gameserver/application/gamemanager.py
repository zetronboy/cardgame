# holds collection of games

# gameserver plugin interface
# new([players]) returns gameid
# redirect players to blueprint /[game]/id=[game_id] url

# holds list of games
# accepts player reg with games offer they want to play

from random import randint
from os import path
from gameserver import log,game_list
import requests

class GameManager():
	POINTER_FILE = 'last_game.ptr'
	def __init__(self):
		self.games = {} # {"12345": {"game":"tcg", "players":["111","222"]}

	def add(self, game_type:str, players):
		"""
		creates new game object of game_type
		inserts game into games list with players
		"""
		"""
		request blueprint api to create new game and return id
		base url on game_type string
		register players in new game request to limit who can access
		like a community in snmp
		"""
		r = requests.post(f'http://{game_type}/new', data = {'players': players})
		if r.status_code == 200:
			game_id = r.json()
			self.games[game_id] = {"game": game_type,
								   "players": players }

	def delete(self, game_id):
		"""
		use the web api to delete a game
		"""
		game_type = self.games[game_id].get("game") # like tcg
		r = requests.get(f'http://{game_type}/delete/{game_id}')
		if r.status_code == 200:
			del self.games[game_id]
			return True