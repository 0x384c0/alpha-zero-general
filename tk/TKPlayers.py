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


def int_to_bool_string(int):
    return "\033[32mYES\033[0m" if int > 0 else "\033[31mNO\033[0m"