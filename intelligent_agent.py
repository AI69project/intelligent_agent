
from api import State, util
import random

class Bot:

    def __init__(self):

    def get_move(self, state):
        player = state.whose_turn() #player on move
        moves = state.moves() #legal moves