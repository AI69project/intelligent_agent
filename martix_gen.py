import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as pyplot


CARD_AMOUNT = 20

#defining card value based on index
def value(index):
    if index%5 == 0:
        return 11
    elif index%5 == 1:
        return 10
    elif index%5 == 2:
        return 5
    elif index%5 == 3:
        return 4
    else:
        return 3

class Matrix:
    #class for matrix
    def __init__(self,size):
        self.size = size
        self.matrix = np.matrix(np.ones(shape=(self.size,self.size)))
        self.matrix *= -1

"""
CLUB,DIAMOND,HEART,SPADE
0,5,10,15 - Ace
1,6,11,16 - 10
2,7,12,17 - King
3,8,13,18 - Queen
4,9,14,19 - Jack
"""

class Generator:
    def __init__(self,firstMove, trumpCard):
        self.firstMove = firstMove
        self.trumpCard = trumpCard

        self.matrix = None
    def populator(self):

        #generate all card pairs
        #format: [card_player_1, card_player_2]
        combinations = []
        for i in range(CARD_AMOUNT):
            for j in range(CARD_AMOUNT ):
                combinations.append([i, j])
        # print(combinations)

        if self.firstMove == True:
            self.matrix = Matrix(CARD_AMOUNT)
            trump = int(self.trumpCard/5) #get the suite of the trump card
            """
            suite_player = int(pair[0]/5) #get suite of the players card
            suite_opponent = int(pair[1]/5) #get suite of the opponent
            """

            for pair in combinations:
                for element in pair:
                    if int(element/5) == trump:
                        element *=10

                if pair[0]== pair[1]:
                    self.matrix[pair[0],pair[1]] = -1 #rule out illegal moves
                else:
                    self.matrix[pair[0], pair[1]] = value(pair[0]) / value(pair[1]) #evaluate moves (winning moves have higher scores)


        """
        default = Matrix(20)
        opn = Matrix(20)
        for pair in combinations:
            if pair[0] == pair[1]:
                default.matrix[pair[0], pair[1]] = -1
                opn.matrix[pair[0], pair[1]] = -1
            else:
                default.matrix[pair[0], pair[1]] = value(pair[0]) / value(pair[1])
                opn.matrix[pair[0], pair[1]] = value(pair[0]) / value(pair[1])

            if pair[0] % 5 == pair[1] % 5:
                opn.matrix[pair[0], pair[1]] = 0
            

pyplot.matshow(default.matrix,cmap=pyplot.cm.hot)
pyplot.matshow(opn.matrix,cmap=pyplot.cm.hot)
pyplot.show()
"""
