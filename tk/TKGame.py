import sys
sys.path.append('..')
from Game import Game
from .TKLogic import Board
import numpy as np


def debug_print(data):
    print('\033[95m' + sys._getframe(1).f_code.co_name + '\033[0m' + '\n' + '\033[92m' + str(data) + '\033[0m')


class TKGame(Game):
    def __init__(self):
        pass

    def getInitBoard(self):
        b = Board()
        debug_print(np.array(b.pieces))
        return np.array(b.pieces)

    def getBoardSize(self):
        debug_print(Board.size)
        return Board.size

    def getActionSize(self):
        debug_print(Board.action_size)
        return Board.action_size

    def getNextState(self, board, player, action):
        b = Board()
        b.pieces = np.copy(board)
        b.execute_move(move, player)
        debug_print("action: " + str(action) + " -> " + str((b.pieces, -player)))
        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        b = Board()
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player)
        debug_print(np.array(legalMoves))
        return np.array(legalMoves)

    def getGameEnded(self, board, player):
        b = Board(self.n)
        b.pieces = np.copy(board)

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
        debug_print(player*board)
        return player*board

    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        
        debug_print(l)
        return l

    def stringRepresentation(self, board):
        debug_print(board.tostring())
        return board.tostring()


def display(board):
    print(board)