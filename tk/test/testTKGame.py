import unittest

import sys
sys.path.append('..')


from ..TKLogic import Board
from ..TKGame import TKGame as Game, display
from utils import *


class TestTKGame(unittest.TestCase):
	def setUp(self):
		self.game = Game()
		self.board = Board()
		self.display = display

	def tearDown(self):
		self.board = None

	def testCanonicalForm(self):

		board = self.board.execute_move(0, 1)
		
		canonical_form_p1 = self.game.getCanonicalForm(board, 1)
		valids_p1 = self.game.getValidMoves(canonical_form_p1,1)
		self.assertEqual(valids_p1.tolist(), [1, 1, 1, 1, 1, 1, 1, 1, 1,	0, 0, 0, 0, 0, 0, 0, 0, 0])

		canonical_form_p2 = self.game.getCanonicalForm(board, -1)
		valids_p2 = self.game.getValidMoves(canonical_form_p2,1)

		self.assertEqual(valids_p2.tolist(), [0, 0, 0, 0, 0, 0, 0, 0, 0,	1, 1, 1, 1, 1, 1, 1, 1, 1])


if __name__ == '__main__':
    unittest.main()