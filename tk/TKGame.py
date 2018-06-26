#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from Game import Game
from .TKLogic import Board
import numpy as np


def debug_print(data):
    pass
    # funcs = [
    # # "getSymmetries",
    # # "getCanonicalForm",
    # "getNextState",
    # ]
    # if sys._getframe(1).f_code.co_name not in funcs:
    #     return
    # print('\033[95m' + sys._getframe(1).f_code.co_name + '\033[0m' + '\n' + '\033[92m' + str(data) + '\033[0m')


class TKGame(Game):
    def __init__(self):
        pass

    def getInitBoard(self):
        b = Board()
        debug_print(np.array(b.get_encoded_state()))
        return np.array(b.get_encoded_state())

    def getBoardSize(self):
        # (a,b) tuple
        debug_print(Board.shape)
        return Board.shape

    def getActionSize(self):
        debug_print(Board.action_size)
        return Board.action_size

    def getNextState(self, board, player, action):
        b = Board()
        b.set_encoded_state(np.copy(board))
        b.execute_move(action, player)
        debug_print("action: " + str(action) + " -> " + str((b.get_encoded_state(), -player)))
        return (b.get_encoded_state(), -player)

    def getValidMoves(self, board, player):
        b = Board()
        b.set_encoded_state(np.copy(board))
        legalMoves =  b.get_legal_moves(player)
        debug_print(np.array(legalMoves))
        return np.array(legalMoves)

    def getGameEnded(self, board, player):
        b = Board() #TODO: add other boars states params
        b.set_encoded_state(np.copy(board))

        if b.is_win(player):
            debug_print("1")
            return 1
        if b.is_win(-player):
            debug_print("-1")
            return -1
        if b.has_legal_moves():
            debug_print("0")
            return 0
        # draw has a very little value 
        debug_print("1e-4")
        return 1e-4

    def getCanonicalForm(self, board, player):
        # if player == 1:
        #     result = board
        # else:
        #     result = board[::-1]
        # debug_print(result)
        return board#result


    def getSymmetries(self, board, pi):
        # no symmetries
        debug_print([(board,pi)])
        return [(board,pi)]


    def stringRepresentation(self, board):
        # debug_print(str(board))
        return str(board)


    def display(self):
        print("\n" + str(self.get_encoded_state()))