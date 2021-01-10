import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as pyplot

"""
CLUB,DIAMOND,HEART,SPADE
0,5,10,15 - Ace
1,6,11,16 - 10
2,7,12,17 - King
3,8,13,18 - Queen
4,9,14,19 - Jack
"""


CARD_AMOUNT = 20
TRUMP_MULTIPLIER = 4

#defining card value based on index
def get_value(index):
    if index%5 == 0: return 11
    elif index%5 == 1: return 10
    elif index%5 == 2: return 5
    elif index%5 == 3: return 4
    else: return 3

def get_suite(index):
    return int(index/5)


class Matrix:
    #class for matrix
    def __init__(self,size):
        self.size = size
        self.matrix = np.matrix(np.ones(shape=(self.size,self.size)))
        self.matrix *= -1


#use the generator with the index of the trump card
#played cards should be array of integer
class Cost_Generator:
    def __init__(self,firstMove, trumpCard, playedCards,playerHand, opponentTrick):
        self.firstMove = firstMove #if the player has the first move
        self.trumpCard = trumpCard #the trump card
        self.playedCards = playedCards #all previous played cards
        self.playerHand = playerHand #the current cards of the player
        self.opponentTrick = opponentTrick #if self.firstMove == False: the card played by opponent

        self.matrix = Matrix(CARD_AMOUNT).matrix #pre-populated Q-matrix



    #checks if a card is present in an array
    #input format : (array, card)
    def is_present(self,playedCards, focalCard):
        for card in playedCards:
            if card == focalCard:
                return True
            else: False


    def populator(self):

        trump = int(self.trumpCard / 5)  # get the suite of the trump card
        combinations = []

        # generate all card pairs
        # format: [card_player_1, card_player_2]
        if self.firstMove == True:
            for i in range(CARD_AMOUNT):
                for j in self.playerHand:
                    combinations.append([i, j])
            # print(combinations)
        else:
            for j in self.playerHand:
                combinations.append([self.opponentTrick, j])


        # calcualte scores
        # format cards
        # populate the matrix
        for pair in combinations:

            suite_player = get_suite(pair[0])  # get suite of the players card
            suite_opponent = get_suite(pair[1])  # get suite of the opponent

            value_player = get_value(pair[0])  # value of the players card
            value_opponent = get_value(pair[1])  # value of the opponents card

            # adjust card value if trump
            if suite_player == trump:
                value_player *= TRUMP_MULTIPLIER
            if suite_opponent == trump:
                value_opponent *= TRUMP_MULTIPLIER

            # populate matrix with score
            if pair[0] == pair[1]:
                self.matrix[pair[0], pair[1]] = -1  # rule out illegal moves
            elif self.is_present(self.playedCards, pair[0]) == True or self.is_present(self.playedCards, pair[1]) == True:
                self.matrix[pair[0], pair[1]] = -1  # blackout moves with unavaliable cards
            else:
                self.matrix[pair[0], pair[1]] = value_player / value_opponent  # evaluate moves (winning moves have higher scores)
