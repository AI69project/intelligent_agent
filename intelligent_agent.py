from . import martix_gen
import matplotlib
import numpy as np
import matplotlib.pyplot as pyplot
from api import State, util
import random

"""
#test matrix
playedCards = [1,12,9,6,2]
playerHand = [3,5,15,16,7]
opponentTrick = 13
one = martix_gen.Cost_Generator(True, "C" ,playedCards,playerHand,opponentTrick)
one.populator()
print(one.matrix)

pyplot.matshow(one.matrix, cmap=pyplot.cm.hot)
pyplot.show()
"""
CARDS_IN_GAME = 20
class Bot:

    def __init__(self):
        self.gamma = 0.8
        self.Q_matrix = martix_gen.Matrix(CARDS_IN_GAME, 0).matrix
        pass

    def get_hand(self, moves):
        playerHand = []
        for move in moves:
            if move[0] is not None and move[1] is None:
                playerHand.append(move[0])
                trump_ex = False
            elif move[0] is None:
                playerHand = move #if trump exchange is available, play it
                trump_ex = True

        return playerHand, trump_ex

    def cards_left(self, card_list, playerHand, playedCards):
        comparison = np.concatenate((playerHand,playedCards))
        new_list = []
        print(comparison)
        for card in comparison:
            for element in card_list:
                if int(element) != int(card):
                    new_list.append(element)
        print(list(dict.fromkeys(new_list)))
        return new_list

    def select_move(self,playerHand, R_matrix , opponentPlayedCard):
        if opponentPlayedCard is None:
            move_selection = R_matrix[playerHand,] #selection of all possible moves with that hand
        else:
            move_selection = R_matrix[playerHand, opponentPlayedCard] # selection of all possible moves with that hand considering already played card.t
        #print(playerHand)
        #print(move_selection, " intelligent_agent line 53")
        best_move_index = np.where(move_selection == np.max(move_selection))[0] #takes moves with max value
        if len(best_move_index) > 1:
            best_move_index = random.choice(best_move_index)
        move = playerHand[int(best_move_index)]
        #print(move)
        return move


    def get_move(self, state):
        moves = state.moves() #legal moves
        trump_suite = state.get_trump_suit()
        playedCards = [] #all previous played cards
        playerHand = self.get_hand(moves)  # used for the cost matrix
        opponentMove = state.get_opponents_played_card()

        if playerHand[1] == True: #if theres a trump exchange available
            chosen_move = playerHand[0]
            return chosen_move

        available_cards = self.cards_left(list(range(CARDS_IN_GAME)),playerHand[0],playedCards)

        R_matrix = martix_gen.Cost_Generator(state.whose_turn(), trump_suite, playedCards, playerHand[0], opponentMove).populator()

        selected_move = self.select_move(playerHand[0], R_matrix, opponentMove)
        for move in moves:
            if selected_move == move[0]:
                chosen_move = move


        self.brain_update(opponentMove, chosen_move, self.gamma, R_matrix, available_cards)

        print("Trained Q matrix:")
        print(self.Q_matrix / np.max(self.Q_matrix) * 100)
        print(chosen_move)

        return chosen_move

    def brain_update(self, played_card, move, gamma, reward_matrix, available_cards):

        if played_card == None:
            played_card = random.choice(available_cards)

        matrix_row = self.Q_matrix[move[0],]
        optimal_play = np.where(matrix_row  == np.max(matrix_row ))[1]

        if optimal_play.shape[0] > 1:
            optimal_play = int(np.random.choice(optimal_play, size=1))
        else: optimal_play = int(optimal_play)

        max_reward = self.Q_matrix[move[0], optimal_play]


        self.Q_matrix[played_card, move[0]] = reward_matrix[played_card, move[0]] + gamma * max_reward
        print("max reward", reward_matrix[played_card,move] + gamma * max_reward)


