import unittest

import sys
sys.path.append('..')


from ..TKLogic import Board
from ..TKGame import TKGame as Game, display
from utils import *


class TestTKGame(unittest.TestCase):
	def setUp(self):
		self.board = Board()
		self.display = display

	def tearDown(self):
		self.board = None

	def testDsiaplay(self):
		board = self.board.get_encoded_state()
		strBoard1 = str(board)
		self.display(board)
		
		strBoard2 = str(board)
		self.display(board)
		self.assertEqual(strBoard1, strBoard2)


if __name__ == '__main__':
    unittest.main()