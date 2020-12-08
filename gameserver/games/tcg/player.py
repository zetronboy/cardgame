
from .assets import OrcCharacter, HumanCharacter
import random
import traceback # call traceback.format_exc() on exceptions
#import logging
from ...log import *
#logging.basicConfig(filename='log.txt',level=logging.DEBUG)
# debug, info, warning



class Player(object):
	card_deck = []
	active_card = None
	special_card = None #persistent modifier to play
	player_cards = []
	prize_cards = []
	discard_pile = []
	action_points = 0 #spent to perform ___

	def __init__(self,id=''):
		self.deck_size = 60  # todo as argument
		self.initial_hand_size = 7
		self.character_count_in_deck = int(self.deck_size / 2)
		if not id:
			id = 'Player' + str(self.new_player_id())
		self.id = id
		self.new_deck(self.deck_size) #later we should allow them to customize and save/load the deck
		self.shuffle_deck()
		new_character = None
		while new_character is None:
			self.deal_hand_from_deck(self.initial_hand_size)
			new_character = self.pull_character_from_hand()

		self.active_card = new_character


	def __str__(self):
		string_rep = self.__class__.__name__ +'('+ self.id +') points:'+ str(self.action_points)
		if self.active_card: string_rep += '\n active:'+ str(self.active_card)
		if self.special_card: string_rep += '\n special:'+ self.special_card
		for card in self.player_cards:
			string_rep += '\n'
			string_rep += ' hand:'+ str(card.toDict())
		return string_rep

	def toDict(self):
		return { 'id': self.id, 'points': self.action_points, 'active': self.active_card, 'special': self.special_card, 'hand': self.player_cards, 'deck': self.card_deck }

	def new_deck(self, size_of_deck):
		"""populate the player deck with random cards"""
		self.card_deck = []
		for i in range(self.character_count_in_deck): #1/4 deck are characters
			character_name = random.choice(assets.Characters)
			if character_name == 'human':
				self.card_deck.append(assets.HumanCharacter())
			elif character_name == 'orc':
				self.card_deck.append(assets.OrcCharacter())
			#debug('added {} to deck'.format(character_name))

		while len(self.card_deck) < size_of_deck:
			element_name = random.choice(assets.Elements)
			self.card_deck.append(assets.CardBase(element_name))
			#debug('added {} element to deck {}/{}'.format(element_name, len(self.card_deck), size_of_deck))

	def deal_card_from_deck(self):
		"""pull first card from desk into hand and returns it"""
		new_card = self.card_deck.pop()
		self.player_cards.append(new_card)
		return new_card

	def discard_from_hand(self, card):
		"""move card from hand to discard pile
		accepts"""
		if card is int:
			card = self.find_card_by_id(card)
			if card is None: return

		self.discard_pile.append(card)
		self.player_cards.remove(card)

	def find_card_by_id(self, card_id):
		"""returns a card by searching hand, active, and deck"""
		for card in self.player_cards:
			if card.id == card_id: return card
		if not self.active_card is None:
			if self.active_card.id == card_id: return self.active_card
		for card in self.card_deck:
			if card.id == card_id: return card

	def is_active_card(self, card):
		"""T/F if active passed is the active card or its id"""
		if self.active_card is None: return False
		if card is int:
			if self.active_card.id == card: return True
		else:
			if self.active_card.id == card.id: return True

	def add_card_to_hand(self, card):
		"""moves the passed card or cardID to hand"""
		if card is int:
			card = self.find_card_by_id(card)
			if card is None: return

		self.player_cards.append(card)

	def add_cards_to_hand(self, new_card_list):
		"""move passed cards to hand"""
		self.player_cards.extend(new_card_list)

	def find_character_in_hand(self):
		"""get the first char from the deck"""
		for card in self.player_cards:
			if card.type in assets.Characters:
				return card

	def pull_character_from_hand(self):
		"""pulls a character card out of the hand"""
		card = self.find_character_in_hand()
		if card:
			self.player_cards.remove(card)
			return card

	def deal_hand_from_deck(self, card_count):
		"""give the player """
		self.player_cards = []
		for i in range(card_count):
			card = self.card_deck.pop()
			self.player_cards.append(card)

		debug('dealt new hand {}'.format(self.player_cards))

	def shuffle_deck(self):
		random.shuffle(self.card_deck)

def debug(message):
	print(message)
	log.debug(message)

def warn(message):
	print("WARN",message)
	log.warning(message)

def error(message):
	print("ERROR",message)
	log.error(message)

if __name__ == '__main__':
	#selftest
	log.startlogging()
	p=Player('selftest')
	print(p)