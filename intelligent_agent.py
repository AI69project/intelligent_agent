import martix_gen
import matplotlib
import matplotlib.pyplot as pyplot
from api import State, util
import random

"""
#test matrix
playedCards = [1,12,9,6,2]
playerHand = [3,5,15,16,7]
opponentTrick = 13
one = martix_gen.Cost_Generator(True, 19,playedCards,playerHand,opponentTrick)
one.populator()
print(one.matrix)

pyplot.matshow(one.matrix, cmap=pyplot.cm.hot)
pyplot.show()
"""
class Bot:

    def __init__(self):
        pass
    def get_move(self, state):
        moves = state.moves() #legal moves
        chosen_move = random.choice(moves)  # initialise chosen move as random by default

        trump_suite = state.get_trump_suit()

        playedCards = [] #all previous played cards
        initial_turn = True #if you have the initial turn or not

        playerHand = []#used for the cost matrix
        for move in moves:
            if move[0] is not None: playerHand.append(move[0])
            else: chosen_move = move #if trump exchange is available, play it

        if state.get_opponents_played_card() is not None:
            initial_turn = False
            opponentTrick = state.get_opponents_played_card()
        else:
            initial_turn = False
            opponentTrick = None



        return chosen_move