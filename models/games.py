from collections import defaultdict
import uuid
from models.chess.game import Game
from random import randint

games = {}
player_queue = []

game_state = defaultdict(dict)

def add_player_to_queue(player_id):
    if player_id in player_queue:
        return -1
    for game in games:
        if player_id in games[game]['players']:
            return -1
    player_queue.append(player_id)
    return len(player_queue)

def remove_player_from_queue(player_id):
    if player_id in player_queue:
        player_queue.remove(player_id)


def create_game(player1, player2):
    
    game_id = str(uuid.uuid4())
    games[game_id] = {
        'players': [player1, player2][::randint(0, 1) * 2 - 1],
        'game': Game(first_player=player1, second_player=player2)
    }
    return game_id