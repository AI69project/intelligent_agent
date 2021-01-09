import martix_gen
import matplotlib
import matplotlib.pyplot as pyplot
#from api import State, util
import random


#
one = martix_gen.Generator(True, 19)
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