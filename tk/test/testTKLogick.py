import unittest

import sys
sys.path.append('..')

from ..TKLogick import Board
from ..utils import *

class TestTKLogick(unittest.TestCase):
	def setUp(self):
		self.board = Board()

	def tearDown(self):
		self.board = None


	def test_get_legal_moves(self):
		self.assertEqual(self.board.get_legal_moves(1), 	[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
		self.assertEqual(self.board.get_legal_moves(-1), 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1])

	def test_has_legal_moves(self):
		self.assertEqual(self.board.has_legal_moves(), 	True)

	def test_is_win(self):
		self.assertEqual(self.board.is_win(1),		False)
		self.assertEqual(self.board.is_win(-1),		False)

	def test_execute_move(self):
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(1,1)),		[9, 1, 10, 10, 10, 10, 10, 10, 10,		0,  9, 9, 9, 9, 9, 9, 9, 9])
		self.assertEqual(self.board.get_player_score(1),10)
		self.assertEqual(self.board.get_player_score(-1),0)
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(1,-1)),		[9, 1, 10, 10, 10, 10, 10, 10, 10,		10, 9, 9, 9, 9, 9, 9, 9, 9])
		self.assertEqual(self.board.get_player_score(1),10)
		self.assertEqual(self.board.get_player_score(-1),0)
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(15,1)),		[10, 10, 10, 10, 10, 10, 9, 9, 9,		9, 9, 9, 9, 9, 9, 1, 10, 10])
		self.assertEqual(self.board.get_player_score(1),10)
		self.assertEqual(self.board.get_player_score(-1),0)
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(15,-1)),	[10, 10, 10, 10, 10, 0,  9, 9, 9,		9, 9, 9, 9, 9, 9, 1, 10, 10])
		self.assertEqual(self.board.get_player_score(1),10)
		self.assertEqual(self.board.get_player_score(-1),10)


if __name__ == '__main__':
    unittest.main()