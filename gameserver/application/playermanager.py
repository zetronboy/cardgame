from gameserver import log

class PlayerManager():
    def __init__(self):
        self.players = {}  # {'192.168.1.123': {'nick': 'joey', 'status':'available', 'games': ['tcg']}}

    def add(self, id:str, nick:str, game_subscriptions):
        #game_subscriptions is a list of games they want to play
        if id not in self.players:
            self.players[id] = {'nick': nick, 'games': game_subscriptions}
        else:
            log.info("Player {nick} is already in the PlayerManager, updating")
            self.update(id, nick, game_subscriptions)

    def update(self, id:str, nick:str, game_subscriptions):
        if id in self.players:
            self.players[id] = {'nick': nick, 'games': game_subscriptions}

    def subscriptions(self, player_id):
        if player_id in self.players:
            return self.players[player_id].get('games')
        else:
            for player in self.players:
                if player.get('nick') == player_id:
                    return player.get('games')

    def status(self, player_id):
        if player_id in self.players:
            return self.players[player_id].get('status')
        else:
            for player in self.players:
                if player.get('nick') == player_id:
                    return player.get('status')

    def nick(self, player_id):
        if player_id in self.players:
            return self.players[player_id].get('nick')