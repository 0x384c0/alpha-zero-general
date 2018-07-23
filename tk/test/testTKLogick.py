import unittest

import sys
sys.path.append('..')

from TKLogic import Board
from TKLogic import MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE, BOARD_SIZE, WIN_SCORE
from utils import *

def generate_encoded_state(state):
	result = data_array_to_one_hot(state[0:18],				MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE) #TODO: remove
	result.append(number_to_bits_array(state[18],		MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE))
	result.append(number_to_bits_array(state[19],		MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE))
	result.append(number_to_onehot(state[20],			MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE))
	result.append(number_to_onehot(state[21],			MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE))


	pieces = state[0:18]
	mid=int((len(pieces) + 1) / 2)

	firstHalf = data_array_to_one_hot_with_shape(pieces[:mid],		(11,MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE))
	firstHalf[9] = number_to_bits_array(state[18],				MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
	firstHalf[10] = number_to_onehot(state[20],					MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)

	secondHalf = data_array_to_one_hot_with_shape(pieces[mid:],		(11,MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE))
	secondHalf[9] = number_to_bits_array(state[19],				MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
	secondHalf[10] = number_to_onehot(state[21],				MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)

	secondHalf *= -1

	result = np.concatenate((firstHalf, secondHalf), axis=0)

	return result

def parse_encoded_state(state):

	HALF_BOARD_SIZE = int(BOARD_SIZE/2)
	mid=int((len(state) + 1) / 2)
	firstHalf = state[:mid]
	secondHalf = state[mid:]
	firstSum = 0
	secondSum = 0



	for onehot in firstHalf:
		firstSum += sum(onehot)

	for onehot in secondHalf:
		secondSum += sum(onehot)

	if firstSum > 0 or secondSum < 0: # playe 1 in firstHalf
		pass
	else: #player -1 in firstHalf
		firstHalf,secondHalf = secondHalf,firstHalf

	secondHalf *= -1 #at this point second half always contains negative numbers



	result =		one_hot_batch_to_array(firstHalf[:HALF_BOARD_SIZE])
	result +=		one_hot_batch_to_array(secondHalf[:HALF_BOARD_SIZE])

	result.append(bits_array_to_number(firstHalf[HALF_BOARD_SIZE]))
	result.append(bits_array_to_number(secondHalf[HALF_BOARD_SIZE]))
	result.append(onehot_to_number(firstHalf[HALF_BOARD_SIZE + 1]))
	result.append(onehot_to_number(secondHalf[HALF_BOARD_SIZE + 1]))
	return result



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

		self.board.set_pieces([9, 9, 9, 9, 9, 9, 5, 9, 9,		9, 2, 9, 9, 9, 9, 9, 9, 9])
		self.board.execute_move(6,1)
		self.board.execute_move(7,1)

		self.assertEqual(self.board.get_legal_moves(1), 	[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0])

	def test_has_legal_moves(self):
		self.assertEqual(self.board.has_legal_moves(), 	True)

	def test_is_win(self):
		state = [9, 9, 9, 9, 9, 9, 9, 9, 9,		9, 9, 9, 9, 9, 9, 9, 9, 9,		WIN_SCORE - 1,1,		None,None]
		self.board.set_encoded_state(generate_encoded_state(state))
		self.assertEqual(self.board.is_win(1),		False)
		self.assertEqual(self.board.is_win(-1),		False)
		self.board.execute_move(1,1)
		self.assertEqual(self.board.is_win(1),		True)

	def test_execute_move(self):
		self.assertEqual(parse_encoded_state(self.board.execute_move(0,1)),		[1, 10, 10, 10, 10, 10, 10, 10, 10,		9,  9, 9, 9, 9, 9, 9, 9, 9,				0, 0, None, None])
		self.setUp()
		self.assertEqual(parse_encoded_state(self.board.execute_move(1,1)),		[9, 1, 10, 10, 10, 10, 10, 10, 10,		0,  9, 9, 9, 9, 9, 9, 9, 9,				10, 0, None, None])
		self.setUp()
		self.assertEqual(parse_encoded_state(self.board.execute_move(9,-1)),	[9, 9, 9, 9, 9, 9, 9, 9, 9,				1, 10, 10, 10, 10, 10, 10, 10, 10,		0, 0, None, None])
		self.setUp()
		self.assertEqual(parse_encoded_state(self.board.execute_move(6,1)),		[9, 9, 9, 9, 9, 9, 1, 10, 10,			10, 10, 10, 10, 10, 0, 9, 9, 9,			10, 0, None, None])
		self.setUp()
		self.assertEqual(parse_encoded_state(self.board.execute_move(15,-1)),	[10, 10, 10, 10, 10, 0,  9, 9, 9,		9, 9, 9, 9, 9, 9, 1, 10, 10,	0, 10, None, None])
		
		self.assertEqual(parse_encoded_state(self.board.execute_move(0,1)),		[1, 11, 11, 11, 11, 1,  10, 10, 10,		0, 9, 9, 9, 9, 9, 1, 10, 10,	10, 10, None, None])
		
		self.board.set_encoded_state(generate_encoded_state( 					[9, 9, 9, 9, 9, 9, 9, 9, 9,				25, 9, 9, 9, 9, 9, 9, 9, 9,				0, 0, 	None, None]))
		self.assertEqual(parse_encoded_state(self.board.execute_move(9,-1)),	[10, 10, 10, 10, 10, 10, 10, 10, 10,	2, 11, 11, 11, 11, 11, 11, 10, 10,		0, 0, 	None, None])

		self.board.set_encoded_state(generate_encoded_state( 					[3, 9, 9, 0, 0, 0, 0, 0, 0,				0, 0, 0, 0, 0, 0, 0, 0, 0,				70, 20,	None, None]))
		self.assertEqual(parse_encoded_state(self.board.execute_move(0,1)),		[0, 0, 0, 0, 0, 0, 0, 0, 0,				0, 0, 0, 0, 0, 0, 0, 0, 0,				91, 20,	None, None])
		self.assertEqual(self.board.is_win(1),True)


	def test_tuz(self):
		self.board.set_pieces([9, 9, 9, 9, 9, 9, 9, 10, 10,		9, 9, 9, 9, 9, 9, 9, 1, 2])
		
		self.assertEqual(parse_encoded_state(self.board.execute_move(8,1)),		[9, 9, 9, 9, 9, 9, 9, 10, 1,	10, 10, 10, 10, 10, 10, 10, 2, 3,		0, 0, 	None, None])
		self.assertEqual(self.board.get_legal_moves(1),							[1, 1, 1, 1, 1, 1, 1, 1, 1,		0, 0, 0, 0, 0, 0, 0, 0, 0])
		
		self.assertEqual(parse_encoded_state(self.board.execute_move(7,1)),		[9, 9, 9, 9, 9, 9, 9, 1, 2,		11, 11, 11, 11, 11, 11, 11, 0, 3,		3, 0, 	16, None])
		self.assertEqual(parse_encoded_state(self.board.execute_move(9,-1)),	[10, 0, 9, 9, 9, 9, 9, 1, 2,	1, 12, 12, 12, 12, 12, 12, 1, 4,		3, 10,	16, None])
		self.assertEqual(self.board.get_legal_moves(1),							[1, 0, 1, 1, 1, 1, 1, 1, 1,		0, 0, 0, 0, 0, 0, 0, 1, 0])

		self.setUp()
		self.board.set_pieces([1, 2, 4, 6, 20, 16, 13, 0, 1,	1, 2, 2, 1, 1, 7, 3, 2, 5])
		self.board.execute_move(0,1)
		self.assertEqual(self.board.get_tuz(),		{1: None, -1: None})

		self.setUp()
		self.board.set_pieces([1, 1, 2, 3, 1, 1, 8, 6, 15,	1, 2, 1, 16, 3, 4, 3, 1, 5])
		self.board.get_tuz()[-1] = 1
		self.assertEqual(self.board.get_legal_moves(-1),							[0, 1, 0, 0, 0, 0, 0, 0, 0,		1, 1, 1, 1, 1, 1, 1, 1, 1,])
		self.board.get_tuz()[-1] = 0
		self.assertEqual(self.board.get_legal_moves(-1),							[1, 0, 0, 0, 0, 0, 0, 0, 0,		1, 1, 1, 1, 1, 1, 1, 1, 1,])



	def test_encoded_state(self):
		state = 	[9, 9, 9, 9, 1, 9, 9, 9, 9,		9, 9, 9, 9, 9, 9, 9, 9, 9,		1,16,		1,None]
		state_rev = [9, 9, 9, 9, 9, 9, 9, 9, 9,		9, 9, 9, 9, 1, 9, 9, 9, 9,		16, 1,		None, 1]
		self.board.set_encoded_state(generate_encoded_state(state))
		self.assertEqual(state, parse_encoded_state(self.board.get_encoded_state()))
		self.assertEqual(state_rev, parse_encoded_state(self.board.get_encoded_state(-1)))

		self.board.set_encoded_state(generate_encoded_state(state))
		canonical_board_for_player = self.board.get_encoded_state()
		canonical_board_for_other_player = self.board.get_encoded_state(-1)
		self.assertEqual(str(self.board.get_encoded_state()),str(self.board.get_encoded_state(-1) * -1))
		self.board.set_encoded_state(canonical_board_for_other_player)
		self.assertEqual(parse_encoded_state( canonical_board_for_player),parse_encoded_state(self.board.get_encoded_state(-1)))

		state_enc = generate_encoded_state(state)
		self.board.set_encoded_state(state_enc)
		state1 = parse_encoded_state(self.board.get_encoded_state())
		
		self.board.set_encoded_state(state_enc)
		state2 = parse_encoded_state(self.board.get_encoded_state())

		self.assertEqual(state1,state2)

	def testDisplay(self):

		state = 	generate_encoded_state([9, 9, 9, 9, 1, 9, 9, 9, 9,		9, 9, 9, 9, 9, 9, 9, 9, 9,		1,16,		1,None])
		
		self.board.set_encoded_state(state)
		str1 = self.board.display()
		
		self.board.set_encoded_state(state)
		str2 = self.board.display()
		self.assertEqual(str1,str2)

if __name__ == '__main__':
    unittest.main()