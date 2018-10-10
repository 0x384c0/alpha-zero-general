import random
import copy
import numpy as np

from tk.TKGame import TKGame as Game
from tk.TKGame import Board, WIN_SCORE
from tk.keras.NNet import NNetWrapper as nn
from tk.test.testTKLogick import generate_encoded_state, parse_encoded_state
from tk.keras.NNet import NNetWrapper as NNet
from keras.utils import Progbar

from utils import *

NUM_ITERS = 100 #number_of_train_iterations()
NUM_STEPS = 1000

INVALID_ACTION_REWARD = -1

def random_argmax(array):
	MAX_DIFF = 2
	arg_max = np.argmax(array)
	max_value = array[arg_max]

	max_value_ids = [arg_max,arg_max,arg_max]

	for idx, value in enumerate(array):
		if value != INVALID_ACTION_REWARD and max_value - value <= MAX_DIFF:
			max_value_ids.append(idx)

	return random.choice(max_value_ids)


def generate_train_batch(num_steps):
	input_boards = []
	target_pis = []
	target_vs = []

	board = Board()
	game = Game()

	player = 1

	print "generate_train_batch"
	progbar = Progbar(num_steps)
	for x in range(num_steps):
		progbar.add(1)

		encoded_state = board.get_encoded_state()
		validMoves = game.getValidMoves(encoded_state, player)




		rewards = []
		for i, action in enumerate(validMoves):
			if action == 1:
				next_encoded_state = game.getNextState(encoded_state, player, i)[0]
				current_score = board.get_players_scores()[player]

				next_board = Board()
				next_board.set_encoded_state(next_encoded_state)
				next_score = next_board.get_players_scores()[player]

				reward = next_score - current_score

				rewards.append(reward)
			else:
				rewards.append(INVALID_ACTION_REWARD) # invalid action


		best_action = random_argmax(rewards)

		game_ended = game.getGameEnded(encoded_state, player)

		if rewards[best_action] != INVALID_ACTION_REWARD and game_ended == 0:
			input_board = game.getCanonicalForm( copy.deepcopy(encoded_state), player)

			encoded_state = board.execute_move(best_action, player)
			score = board.get_players_scores()[player]
			action_onehot = number_to_onehot(best_action,Board.action_size)
			win_probability = float(score) / float(WIN_SCORE)


			player *= -1

			input_boards.append(input_board)
			target_pis.append(action_onehot)
			target_vs.append(win_probability)

			# print "\n"
			# print parse_encoded_state(input_board)
			# print "reward " + str(rewards[best_action]) + " of " + str(rewards)
			# print outputs
		else:
			player == 1
			board = Board() # no valid actions or game ended, reset board
			encoded_state = board.get_encoded_state()

	return input_boards, target_pis, target_vs




# training

g = Game()
n1 = NNet(g)
n1.load_checkpoint('temp',"best_heuristic.h5")
n1.nnet.model._make_predict_function()

for i in range(NUM_ITERS):
	print "iteration " + str(i) + " / " + str(NUM_ITERS)
	input_boards, target_pis, target_vs = generate_train_batch(NUM_STEPS)
	input_boards = np.asarray(input_boards)
	target_pis = np.asarray(target_pis)
	target_vs = np.asarray(target_vs)

	n1.nnet.model.fit(x = input_boards, y = [target_pis, target_vs], batch_size = int(NUM_STEPS * .6), epochs = 5)

	if i % 5 == 0:
		n1.save_checkpoint('temp',"best_heuristic.h5")

loss = n1.nnet.model.test_on_batch(x = input_boards, y = [target_pis, target_vs])
print loss


# others

# state = [2, 2, 2, 2, 2, 2, 2, 2, 2, 3,		2, 3, 2, 2, 2, 2, 2, 2, 0, 0, None, None]
# encoded_state = generate_encoded_state(state)


# board = Board()
# encoded_state = board.get_encoded_state()

# print encoded_state

# board.set_encoded_state(encoded_state)

# print board.get_pieces()
# print board.get_players_scores()
# print board.get_players_tuz()
