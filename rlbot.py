import numpy as np
import random
from api import Deck

CARDS = list(range(20))


class Bot:
    def __init__(self):
        pass
        self.global_av_cards = CARDS

    def get_suite(self,index):
        suits = ["C","D","H","S"]
        return suits[int(index/5)]

    def get_move(self,state):
        self.played_cards = state.get_prev_trick() if state.get_prev_trick() != [None, None] else []
        self.trump_suite = state.get_trump_suit()
        self.total_points = state.get_points(1) + state.get_points(2)

        #get Q-Matrix
        self.Q_matrix = np.loadtxt(file := open("Q_matrix.csv", "rb"), delimiter=",")
        file.close()
        #format Q-Matrix for trump suite
        for i in range(20):
            if self.get_suite(i) == self.trump_suite:
                self.Q_matrix[i,] *= 6
                self.Q_matrix[:,i] *= 6

        moves = state.moves()
        chosen_move = random.choice(moves) #initialise chosen_move
        hand = self.get_hand(moves) #get the cards in hand

        # if theres a trump exchange available
        if hand[1] == True:
            chosen_move = hand[0]
            return chosen_move

        #get the move selection Matrix
        if state.get_opponents_played_card() == None:
            move_selection = self.Q_matrix[hand[0],]
        else:
            move_selection = self.Q_matrix[hand[0],state.get_opponents_played_card()]
            for i in range(len(hand[0])):
                if self.get_suite(i) != self.get_suite(state.get_opponents_played_card()) and self.get_suite(i) != self.trump_suite:
                    move_selection[i,] *= 0.6

            self.played_cards.append(state.get_opponents_played_card())
        self.get_av_cards([hand[0], self.played_cards]) #update av cards

        chosen_card = self.get_best_move(state, move_selection, hand[0])
        #select move from hand
        for move in moves:
            if chosen_card == move[0]:
                chosen_move = move

        return chosen_move

    def get_hand(self, moves):
        playerHand = []
        trump_ex = False
        for move in moves:
            if move[0] is not None and move[1] is None:
                playerHand.append(move[0])
            elif move[0] is None:
                playerHand = move  # if trump exchange is available, play it
                trump_ex = True
        return playerHand, trump_ex

    def get_best_move(self, state, move_selection, hand):
        av_cards = self.global_av_cards
        current_hand = hand
        value = 0
        best_move = None

        def next_state_val():
            next_moves = next_state.moves()
            next_hand = self.get_hand(next_moves)

            for card in next_hand:
                if card in av_cards:
                    av_cards.remove(card)
            q_val = np.sum(self.Q_matrix[np.ix_(next_hand[0], av_cards)])
            return q_val

        for row, card in enumerate(current_hand):
            next_state = state.next((card, None)) if state.get_phase() == 2 else state.make_assumption()

            q_val_current = np.sum(move_selection[row,])
            q_val_next = next_state_val()

            temp_value = q_val_current + q_val_next

            if temp_value > value:
                value = temp_value
                best_move = card

        return best_move

    def get_av_cards(self, known_cards):#get all unknown cards
        if self.total_points == 0:
            self.global_av_cards = CARDS

        for array in known_cards:
            for card in array:
                if card in self.global_av_cards:
                    self.global_av_cards.remove(card)



