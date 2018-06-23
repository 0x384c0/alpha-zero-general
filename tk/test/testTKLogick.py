import unittest

import sys
sys.path.append('..')

from TKLogic import Board
from TKLogic import MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE
from utils import *

class TestTKLogic(unittest.TestCase):
	def setUp(self):
		self.board = Board()

	def tearDown(self):
		self.board = None


	def test_get_legal_moves(self):
		self.assertEqual(self.board.get_legal_moves(1), 	[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
		self.assertEqual(self.board.get_legal_moves(-1), 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1])
		
		self.board.execute_move(1,1)
		self.board.execute_move(1,1)
		self.assertEqual(self.board.get_legal_moves(1),		[1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])

		self.board.pieces = data_array_to_one_hot([9, 9, 9, 9, 9, 9, 5, 9, 9,		9, 2, 9, 9, 9, 9, 9, 9, 9],MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
		self.board.execute_move(6,1)
		self.board.execute_move(7,1)
		self.assertEqual(self.board.get_legal_moves(1), 	[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0])

	def test_has_legal_moves(self):
		self.assertEqual(self.board.has_legal_moves(), 	True)

	def test_is_win(self):
		self.assertEqual(self.board.is_win(1),		False)
		self.assertEqual(self.board.is_win(-1),		False)
		self.board.set_player_score(80,1)
		self.board.execute_move(1,1)
		self.assertEqual(self.board.is_win(1),		True)

	def test_execute_move(self):
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(1,1)),		[9, 1, 10, 10, 10, 10, 10, 10, 10,		0,  9, 9, 9, 9, 9, 9, 9, 9])
		self.assertEqual(self.board.get_player_score(1),10)
		self.assertEqual(self.board.get_player_score(-1),0)
		self.setUp()
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(1,-1)),		[9, 1, 10, 10, 10, 10, 10, 10, 10,		10, 9, 9, 9, 9, 9, 9, 9, 9])
		self.assertEqual(self.board.get_player_score(1),0)
		self.assertEqual(self.board.get_player_score(-1),0)
		self.setUp()
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(15,1)),		[10, 10, 10, 10, 10, 10, 9, 9, 9,		9, 9, 9, 9, 9, 9, 1, 10, 10])
		self.assertEqual(self.board.get_player_score(1),0)
		self.assertEqual(self.board.get_player_score(-1),0)
		self.setUp()
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(15,-1)),	[10, 10, 10, 10, 10, 0,  9, 9, 9,		9, 9, 9, 9, 9, 9, 1, 10, 10])
		self.assertEqual(self.board.get_player_score(1),0)
		self.assertEqual(self.board.get_player_score(-1),10)

		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(0,1)),		[1, 11, 11, 11, 11, 1,  10, 10, 10,		0, 9, 9, 9, 9, 9, 1, 10, 10])
		self.assertEqual(self.board.get_player_score(1),10)
		self.assertEqual(self.board.get_player_score(-1),10)

	def test_tuz(self):
		self.board.pieces = data_array_to_one_hot([9, 9, 9, 9, 9, 9, 9, 10, 10,		9, 9, 9, 9, 9, 9, 9, 1, 2],MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
		
		# print(one_hot_batch_to_array(self.board.pieces))
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(8,1)),		[9, 9, 9, 9, 9, 9, 9, 10, 1, 10, 10, 10, 10, 10, 10, 10, 2, 3])
		self.assertEqual(self.board.get_legal_moves(1),								[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
		
		# print(one_hot_batch_to_array(self.board.pieces))
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(7,1)),		[9, 9, 9, 9, 9, 9, 9, 1, 2,		11, 11, 11, 11, 11, 11, 11, 0, 3])
		self.assertEqual(one_hot_batch_to_array(self.board.execute_move(9,1)),		[10, 10, 9, 9, 9, 9, 9, 1, 2,	1, 12, 12, 12, 12, 12, 12, 1, 4])
		self.assertEqual(self.board.get_legal_moves(1),								[1, 1, 1, 1, 1, 1, 1, 1, 1,		0, 0, 0, 0, 0, 0, 0, 1, 0])





if __name__ == '__main__':
    unittest.main()