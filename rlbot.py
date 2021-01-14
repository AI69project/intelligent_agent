import numpy as np
import random

class Bot:
    def __init__(self):
        pass

    def get_hand(self, moves):
        playerHand = []
        for move in moves:
            if move[0] is not None and move[1] is None:
                playerHand.append(move[0])
                trump_ex = False
            elif move[0] is None:
                playerHand = move  # if trump exchange is available, play it
                trump_ex = True
        return playerHand, trump_ex

    def get_move(self,state):
        Q_matrix = np.loadtxt(file := open("Q_matrix.csv", "rb"), delimiter=",")
        file.close()
        moves = state.moves()
        hand = self.get_hand(moves)

        if hand[1] == True:  # if theres a trump exchange available
            chosen_move = hand[0]
            return chosen_move

        move_selection = Q_matrix[hand[0],] if state.get_opponents_played_card() == None else Q_matrix[hand[0],state.get_opponents_played_card()]
        index = np.where(move_selection == np.max(move_selection))[0]
        chosen_move_card = hand[0][int(random.choice(index))]
        for move in moves:
            if chosen_move_card == move[0]:
                chosen_move = move

        return chosen_move