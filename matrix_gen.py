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
#TRUMP_MULTIPLIER = 6

# changes move tuple to only the card index
def get_hand(moves):
    playerHand = []
    for move in moves:
        if move[0] is not None and move[1] is None:
            playerHand.append(move[0])
            trump_ex = False
        elif move[0] is None:
            playerHand = move  # if trump exchange is available, play it
            trump_ex = True
    return playerHand, trump_ex

#defining card value based on index
def get_value(index):
    if index%5 == 0: return 11
    elif index%5 == 1: return 10
    elif index%5 == 2: return 4
    elif index%5 == 3: return 3
    else: return 2

def get_suite(index):
    if index != None:
        return int(index / 5)
    else: return None

def suite_to_index(suite):
    if suite == "C":
        return 0
    elif suite == "D":
        return 1
    elif suite == "H":
        return 2
    else: return 3

class Matrix:
    #class for matrix
    def __init__(self,size,default_value):
        self.size = size
        self.matrix = np.matrix(np.zeros(shape=(self.size,self.size)))
        self.matrix += default_value


#use the generator with the index of the trump card
#played cards should be array of integer
class Reward_Matrix:
    def __init__(self,whoseTurn, trumpSuite, playedCards,playerHand, opponentTrick):
        self.whoseTurn = whoseTurn #if the player has the first move
        self.trumpSuite = suite_to_index(trumpSuite) #the trump suite
        self.playedCards = playedCards #all previous played cards
        self.playerHand = playerHand #the current cards of the player
        self.opponentTrick = opponentTrick #if self.firstMove == False: the card played by opponent

        self.matrix = Matrix(CARD_AMOUNT, -1).matrix #pre-populated Q-matrix with default value



    #checks if a card is present in an array
    #input format : (array, card)
    def is_present(self,playedCards, focalCard):
        for card in playedCards:
            return True if card == focalCard else False


    def populate(self):
        combinations = []
        # generate all card pairs
        # format: [card_player_1, card_player_2]

        #print(self.whoseTurn)
        #print(self.opponentTrick)
        if self.whoseTurn == 2 and self.opponentTrick != None: #if opponent has played card adapt to it
            for j in self.playerHand:
                combinations.append([self.opponentTrick, j])
        else: #if opponent didnt play card search for best outcome
            for i in range(CARD_AMOUNT):
                for j in self.playerHand:
                    combinations.append([i, j])

        # calcualte scores
        # format cards
        # populate the matrix
        for pair in combinations:
            player = pair[1]
            opponent = pair[0]
            """
            suite_player = get_suite(player)  # get suite of the players card
            suite_opponent = get_suite(opponent)  # get suite of the opponent
            """
            value_player = get_value(player)  # value of the players card
            value_opponent = get_value(opponent)  # value of the opponents card

            # adjust card value if trump
            #value_player *= TRUMP_MULTIPLIER if suite_player == self.trumpSuite else value_player
            #value_opponent *= TRUMP_MULTIPLIER if suite_opponent == self.trumpSuite else value_opponent
            print(player, opponent)

            # populate matrix with score
            if opponent != player:
                if value_player > value_opponent:
                    self.matrix[player, opponent] = (value_player / value_opponent)
                    #print(self.matrix[player, opponent], player, opponent)
                    #self.matrix[pair[1], pair[0]] = value_player / value_opponent   # evaluate moves (winning moves have higher scores)
                else:
                    self.matrix[player, opponent] = value_player / value_opponent
                    #print(self.matrix[player, opponent], player, opponent)
                self.matrix[:,self.playedCards] = -1
            """        
            if opponent == player:
                self.matrix[player, opponent] = -1  # rule out illegal moves
            elif self.is_present(self.playedCards, player) == True or self.is_present(self.playedCards, opponent) == True:
                self.matrix[player, opponent] = -1  # blackout moves with unavaliable cards
                self.matrix[opponent, player] = -1
            else:
                #self.matrix[pair[1], pair[0]] = value_player / value_opponent
            """

        """
        #nomralize all possible moves
        sum = 0
        for i in range(CARD_AMOUNT):
            for j in range(i,CARD_AMOUNT):#i
                sum += self.matrix[i,j] if self.matrix[i,j] >= 0 else sum
                sum += self.matrix[j,i] if self.matrix[j,i] >= 0 else sum
        for i in range(CARD_AMOUNT):
            for j in range(i, CARD_AMOUNT):
                self.matrix[i, j] /= sum if self.matrix[i, j] >= 0 else -1
                self.matrix[j, i] /= sum if self.matrix[j, i] >= 0 else -1
                """
        return self.matrix