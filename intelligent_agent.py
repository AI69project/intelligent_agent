import martix_gen
import pylab as pyplot
from pathlib import Path
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
        self.Q_matrix = martix_gen.Matrix(CARDS_IN_GAME, 0).matrix #problem??

        self.points = 0
        #self.score = []
        pass


    def file_append(self,score):
        #print(str(score), "l33")
        #write scores to file
        with open("bots/intelligent_agent/scores.txt", "a+") as score_file:
            score_file.write(str(score) + "\n")


    #changes move tuple to only the card index
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
        new_list = card_list
        for card in comparison:
            new_list.remove(card)
        return new_list

    def select_move(self,playerHand, R_matrix , opponentPlayedCard):
        if opponentPlayedCard is None:
            move_selection = R_matrix[playerHand,] #selection of all possible moves with that hand
        else:
            move_selection = R_matrix[playerHand, opponentPlayedCard] # selection of all possible moves with that hand considering already played card.t

        best_move_index = np.where(move_selection == np.max(move_selection))[0] #takes moves with max value

        if len(best_move_index) > 1: #if there are multiple moves with same score -> take random one
            best_move_index = random.choice(best_move_index)

        #print(best_move_index)
        move = playerHand[int(best_move_index)]

        return move

    def get_move(self, state):
        new_points = state.get_points(2)#points to be credited from last time

        playedCards = []  # all previous played cards
        #populating playedCards Array if there was a move prior
        if state.get_prev_trick() != [None, None]:
            for element in state.get_prev_trick():
                playedCards.append(element)

        moves = state.moves() #legal moves
        trump_suite = state.get_trump_suit()

        playerHand = self.get_hand(moves)  #players hand of playable cards / used for the cost matrix
        opponentMove = state.get_opponents_played_card()

        if playerHand[1] == True: #if theres a trump exchange available
            chosen_move = playerHand[0]
            return chosen_move

        available_cards = self.cards_left(list(range(CARDS_IN_GAME)),playerHand[0],playedCards)

        R_matrix = martix_gen.Reward_Matrix(state.whose_turn(), trump_suite, playedCards, playerHand[0], opponentMove).populate()

        selected_move = self.select_move(playerHand[0], R_matrix, opponentMove)
        for move in moves: #since selected move is only the card we need to select the move properly
            if selected_move == move[0]:
                chosen_move = move

        #reward falsely
        if self.points == new_points and state.get_points(1) != 0: #if previous trick was loosing, make negativ reward
            self.points += new_points
            #self.score.append(self.brain_update(opponentMove, chosen_move, self.gamma * -1, R_matrix, available_cards))
            self.score = self.brain_update(opponentMove, chosen_move, self.gamma * -1, R_matrix, available_cards)
        else: #else postive reward
            self.points += new_points
            #self.score.append(self.brain_update(opponentMove, chosen_move, self.gamma * 1, R_matrix, available_cards))
            self.score = self.brain_update(opponentMove, chosen_move, self.gamma, R_matrix, available_cards)

        """ 
        print("Trained Q matrix:")
        #print(self.Q_matrix / self.Q_matrix *100)
        print(self.Q_matrix / np.sum(self.Q_matrix))"""

        self.file_append(self.score)
        return chosen_move

    def brain_update(self, opponentMove, move, gamma, reward_matrix, available_cards):

        if opponentMove == None:#if opponent didnt play select random card as opponentMove
            opponentMove = random.choice(available_cards)

        matrix_row = self.Q_matrix[move[0],]
        optimal_play = np.where(matrix_row == np.max(matrix_row))[1]

        if optimal_play.shape[0] > 1:
            optimal_play = int(np.random.choice(optimal_play, size=1))
        else: optimal_play = int(optimal_play)

        max_reward = self.Q_matrix[move[0],optimal_play]


        self.Q_matrix[move[0], opponentMove] = reward_matrix[move[0], opponentMove] + gamma * max_reward
        #print("max reward", reward_matrix[move[0],played_card] + gamma * max_reward)

        return (np.sum(self.Q_matrix / np.max(self.Q_matrix)))


