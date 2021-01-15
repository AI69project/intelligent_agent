from . import matrix_gen
import pylab as pyplot
import numpy as np
import random

"""
#test matrix
playedCards = [1,12,9,6,2]
playerHand = [3,5,15,16,7]
opponentTrick = 13
one = martix_gen.Reward_Matrix(True, "C" ,playedCards,playerHand,opponentTrick).populate()
print(one)

pyplot.matshow(one, cmap=pyplot.cm.hot)
pyplot.show()
"""


CARDS_IN_GAME = 20
class Bot:

    def __init__(self):
        self.gamma = 0.7
        self.Q_matrix = matrix_gen.Matrix(CARDS_IN_GAME, 0).matrix #problem??

        self.points = 0
        #self.score = []
        pass

    #adds scores to txt file for graphs
    def file_append(self,score):
        #print(str(score), "l33")
        #write scores to file
        with open("bots/intelligent_agent/scores.txt", "a+") as score_file:
            score_file.write(str(score) + "\n")

    #makes an array of all cards left unknown to int_agent
    def cards_left(self, card_list, playerHand, playedCards):
        comparison = np.concatenate((playerHand,playedCards))
        new_list = card_list
        for card in comparison:
            new_list.remove(card)
        return new_list

    # selects the next move
    def select_move(self,playerHand, R_matrix , opponentPlayedCard):
        move_selection = R_matrix[playerHand,]
        possible_moves = np.where(move_selection >= 0)[0]
        #selection of all possible moves with that hand

        move = playerHand[int(np.random.choice(possible_moves,1))]
        """
        print(playerHand)
        print(move)"""
        return move

    def get_move(self, state):

        playedCards = []  # all previous played cards
        #populating playedCards Array if there was a move prior
        if state.get_prev_trick() != [None, None]:
            for element in state.get_prev_trick():
                playedCards.append(element)

        moves = state.moves() #legal moves
        trump_suite = state.get_trump_suit()

        playerHand = matrix_gen.get_hand(moves)  #players hand of playable cards / used for the cost matrix
        opponentMove = state.get_opponents_played_card()

        if playerHand[1] == True: #if theres a trump exchange available
            chosen_move = playerHand[0]
            return chosen_move

        available_cards = self.cards_left(list(range(CARDS_IN_GAME)),playerHand[0],playedCards)

        R_matrix = matrix_gen.Reward_Matrix(state.whose_turn(), trump_suite, playedCards, playerHand[0], opponentMove).populate()

        selected_move = self.select_move(playerHand[0], R_matrix, opponentMove)
        for move in moves: #since selected move is only the card we need to select the move properly
            if selected_move == move[0]: chosen_move = move

        self.score = self.brain_update(opponentMove, chosen_move, self.gamma, R_matrix, available_cards)
        self.file_append(self.score)

        print(self.Q_matrix)
        """
        print("Trained Q matrix:")
        #print(self.Q_matrix / self.Q_matrix *100)
        print(self.Q_matrix / np.sum(self.Q_matrix))"""

        np.savetxt("Q_matrix.csv", self.Q_matrix, delimiter= ",", fmt = "%f")

        return chosen_move

    def brain_update(self, opponentMove, move, gamma, reward_matrix, available_cards):
        def shorten_array(optimal_play):
            print(optimal_play)
            if optimal_play.shape[0] > 1:
                # optimal_play = int(np.random.choice(optimal_play, size=1))
                card_val_array = [card % 5 for card in optimal_play]
                i = np.where(card_val_array == np.min(card_val_array))
                optimal_play = np.random.choice(optimal_play[i], 1)
            else: optimal_play = int(optimal_play)
            return optimal_play

        if opponentMove == None:#if opponent didnt play select random card as opponentMove
            opponentMove = np.random.choice(available_cards)#assumes oppontent plays random card
            optimal_play = shorten_array(np.where(self.Q_matrix[move[0],] == np.max(self.Q_matrix[move[0],]))[1])
            max_reward = self.Q_matrix[move[0], optimal_play]
            self.Q_matrix[move[0], opponentMove] = reward_matrix[move[0], opponentMove] + gamma * max_reward
        else: #if opponent already played a card
            optimal_play = shorten_array(np.where(self.Q_matrix[:,opponentMove] == np.max(self.Q_matrix[:,opponentMove]))[0])
            max_reward = self.Q_matrix[optimal_play, opponentMove]
            self.Q_matrix[opponentMove, optimal_play] = reward_matrix[opponentMove, optimal_play] + gamma * max_reward


        #cself.Q_matrix = np.divide(self.Q_matrix,np.max(self.Q_matrix))

        return (np.sum(self.Q_matrix))


