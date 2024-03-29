from .player import Player
from .assets import HumanCharacter, OrcCharacter

from . import log
import json

class Game(object):
	players = []
	last_card_id = 0
	last_player_id = 0
	id = 0
	def __init__(self, id, player1, player2):
		"""stores port for use on connect
		port must be the same on client and server"""
		self.id = id #game id
		self.players.append(Player(player1))
		self.players.append(Player(player2))
		self.turn = 0 # what players turn is it

	def __str__(self):
		return 'Game('+ str(self.id) +')\n P1 '+ str(self.players[0]) +'\n\n P2 '+ str(self.players[1]) #dump obj to str

	def toDict(self):
		"""used to serialize the object for JSON use in websocket emit"""
		return { 'id': self.id, 'player1': self.players[0].toDict(), 'player2': self.players[1].toDict() }

	def attack(self):
		log.debug("attack")
		pass

	def move(self):
		log.debug("move")
		pass

	def draw(self):
		log.debug("draw card")
		pass

	def forefit(self):
		log.debug("forefit")
		pass


	def new_player_id(self):		
		self.last_player_id += 1
		return self.last_player_id


	def new_card_id(self):
		self.last_card_id += 1
		return self.last_card_id

if __name__ == '__main__':
	game = Game(Player(),  Player())
	print(game.toDict())
