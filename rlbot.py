import numpy as np
import random

CARDS = list(range(20))

class Bot:
    def __init__(self):
        pass


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

    """
    def cards_left(self,hand):
        cards = self.global_av_cards
        known_cards = np.concatenate((hand, self.played_cards))
        for card in cards:
            if card in known_cards:
                cards.remove(card)
        return cards"""



    def get_best_move(self,state,move_selection, hand):

        current_hand = hand
        value = 0
        best_move = None

        def next_state_prep(i,value):
            next_moves = next_state.moves()
            next_hand = self.get_hand(next_moves)
            q_val = np.sum(self.Q_matrix[next_hand[0], random.choice(CARDS)])
            temp_val = np.sum(move_selection[:i]) + q_val
            if temp_val > value:
                value = temp_val
                best_move = i


        if len(move_selection.shape) > 1:
            for row, i in enumerate(current_hand):
                next_state = state.next((i, None)) if state.get_phase() == 2 else state.make_assumption()
                next_state_prep(i,value)
        else:
            for element, i in enumerate(current_hand):
                next_state = state.next((element, None)) if state.get_phase() == 2 else state.make_assumption()
                next_state_prep(i,value)
        return best_move


    def get_move(self,state):
        self.played_cards = []
        if state.get_prev_trick() != [None,None]:
            for element in state.get_prev_trick():
                self.played_cards.append(element)

        self.Q_matrix = np.loadtxt(file := open("Q_matrix.csv", "rb"), delimiter=",")
        file.close()

        moves = state.moves()
        chosen_move = random.choice(moves)
        hand = self.get_hand(moves)

        if hand[1] == True:  # if theres a trump exchange available
            chosen_move = hand[0]
            return chosen_move

        if state.get_opponents_played_card() == None:
            move_selection = self.Q_matrix[hand[0],]
        else:
            self.played_cards.append(state.get_opponents_played_card())
            move_selection = self.Q_matrix[hand[0],state.get_opponents_played_card()]

        #self.global_av_cards = self.cards_left(hand[0])
        chosen_card = self.get_best_move(state, move_selection, hand[0])

        """
        index = np.where(move_selection == np.max(move_selection))[0]
        chosen_move_card = hand[0][int(random.choice(index))]
        """
        for move in moves:
            if chosen_card == move[0]:
                chosen_move = move

        return chosen_move