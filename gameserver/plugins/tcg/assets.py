import traceback # call traceback.format_exc() on exceptions
from . import log

Elements = ['water','earth','wind','fire']
Characters = ['human','orc']
#TODO need special affect cards list and classes

import json


class CardBase(object):
    type = None # name of an Elements or Characters
    id = 0

    def __init__(self, card_type):
        self.type = card_type
        self.id = new_card_id()  # cardid used by web to id a card

    def __str__(self):
        return self.type +'('+ str(self.id) +')'

    def toDict(self):
        return { 'type': self.type, 'id': self.id }

class CharacterBase(CardBase):
    level = 0
    hit_points = 100
    character_levels = [
        {'physical': 50, 'special': None},
        {'physical': 50, 'special': None},
        {'physical': 50, 'special': None}
    ]
    defense = {'base': 0.5,
               'physical': 0.5,
               'water': 0,
               'earth': 0,
               'wind': 0,
               'fire': 0
               }
    attack = {'base': 0.5,
              'physical': 0.5,
              'water': 0,
              'earth': 0,
              'wind': 0,
              'fire': 0
              }

    def __init__(self, card_type):
        self.type = card_type
        CardBase.__init__(self, card_type)

    def toDict(self):
        return { 'type': self.type,
                 'id': self.id,
                 'level': self.level,
                 'defense': self.defense,
                 'attack': self.attack
                 }

    def __str__(self):
        return 'type '+ self.type +'('+ str(self.id) +') L=' + str(self.level) + \
               '\n defense ' + str(self.defense) + \
               '\n attack ' + str(self.attack)

    def get_attack_damage(self, character_to_attack):
        pass

    def apply_hit(self, attacking_character):
        print("TODO apply_hit to",attacking_character)

    def is_alive(self):
        return self.hit_points > 0

    def evolve(self):
        if int(self.level) < len(self.character_levels):
            self.level += 1
            print('character has evolved to level', self.level)

class HumanCharacter(CharacterBase):
    type="human" #override base
    hit_points = 100
    def __init__(self):
        CharacterBase.__init__(self, self.type)
    #todo override base class

class OrcCharacter(CharacterBase):
    type='orc'
    def __init__(self):
        CharacterBase.__init__(self, self.type)

#todo create other character card types

if __name__ == '__main__':
    base = CardBase('earth')
    log.debug(base.toDict())
    human = HumanCharacter()
    log.debug(human.toDict())
    orc = OrcCharacter()
    log.debug(orc.toDict())