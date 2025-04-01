import json
import os
from app.game_engine import GameEngine

SAVE_FILE = 'game_save.json'

def save_game(game):
    with open(SAVE_FILE, 'w') as f:
        json.dump(game.to_dict(), f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            game = GameEngine()
            game.from_dict(data)
            return game
    return None
