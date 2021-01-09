import martix_gen
import matplotlib
import matplotlib.pyplot as pyplot
#from api import State, util
import random

#test matrix
playedCards = [1,12,9,6,2]
playerHand = [3,5,15,16,7]
one = martix_gen.Cost_Generator(True, 19,playedCards,playerHand)
one.populator()
print(one.matrix)

pyplot.matshow(one.matrix, cmap=pyplot.cm.hot)
pyplot.show()
"""
class Bot:

    def __init__(self):

    def get_move(self, state):
        player = state.whose_turn() #player on move
        moves = state.moves() #legal moves

"""