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

	def testGetValidMoves(self):
		self.assertEqual(self.game.getValidMoves(self.board.get_encoded_state(),1).tolist(), [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])


if __name__ == '__main__':
    unittest.main()