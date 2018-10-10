import numpy as np
from utils import *

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a


class HumanTKPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid = self.game.getValidMoves(board, 1)
        print("valid?\t" + '\t'.join(map(int_to_bool_string, valid)))
        print("number\t" + '\t'.join(map(str, range(len(valid)))))
        print("Enter any number of valid action, marked " + int_to_bool_string(1) + ":")
        print("\n")


        action_number = None
        while True: 
            a = input()
            try:
                action_number = int(a)
            except ValueError:
                print(red("Error: Not a number"))
                continue

            if action_number < 0 or action_number > len(valid):
                print(str(action_number) + ' is out of range')
                continue

            if valid[action_number] == 0:
                print(str(action_number) + ' is invalid action')
                continue

            print("Selected action is: " + green(action_number))
            break

        return action_number


import random
from tk.TKGame import Board
class HeuristicPlayer():

    INVALID_ACTION_REWARD = -1
    def random_argmax(self, array):
        MAX_DIFF = 1
        arg_max = np.argmax(array)
        max_value = array[arg_max]

        max_value_ids = [arg_max,arg_max,arg_max]

        for idx, value in enumerate(array):
            if value != self.INVALID_ACTION_REWARD and max_value - value <= MAX_DIFF:
                max_value_ids.append(idx)

        return random.choice(max_value_ids)


    def __init__(self, game):
        pass


    def play(self, encoded_state):

        board = Board()
        board.set_encoded_state(encoded_state)
        player = 1
        validMoves = board.get_legal_moves(player)
        current_score = board.get_players_scores()[player]

        rewards = []
        for action, valid in enumerate(validMoves):
            if valid == 1:
                next_board = Board()
                next_board.set_encoded_state(encoded_state)
                next_board.execute_move(action, player)
                next_score = next_board.get_players_scores()[player]

                reward = next_score - current_score
                rewards.append(reward)
            else:
                rewards.append(self.INVALID_ACTION_REWARD) # invalid action

        validRewards = map(lambda x: x if x != -1 else 0,rewards)

        if sum(validRewards) == 0:
            validPieces = board.get_pieces()
            for action,valid in enumerate(validMoves):
                if valid == 0:
                    validPieces[action] = 0
            return np.argmax(validPieces)
        else:
            action = self.random_argmax(rewards)
            return action


def int_to_bool_string(int):
    return "\033[32mYES\033[0m" if int > 0 else "\033[31mNO\033[0m"