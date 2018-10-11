import random
import copy
import numpy as np

from tk.TKPlayers import HeuristicPlayer
from tk.TKGame import TKGame as Game
from tk.TKGame import Board, WIN_SCORE
from tk.keras.NNet import NNetWrapper as nn
from tk.test.testTKLogick import generate_encoded_state, parse_encoded_state
from tk.keras.NNet import NNetWrapper as NNet
from keras.utils import Progbar

from utils import *

NUM_ITERS = number_of_train_iterations()
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
	heuristicPlayer = HeuristicPlayer()

	player = 1

	print("generate_train_batch")
	progbar = Progbar(num_steps)
	for x in range(num_steps):
		progbar.add(1)

		encoded_state = board.get_encoded_state()


		canonical_form = game.getCanonicalForm(encoded_state, player)
		best_action = heuristicPlayer.play(canonical_form)


		game_ended = game.getGameEnded(encoded_state, player)

		if game_ended == 0:
			input_board = game.getCanonicalForm( copy.deepcopy(encoded_state), player)

			encoded_state = board.execute_move(best_action, player)
			score = board.get_players_scores()[player]
			action_onehot = number_to_onehot(best_action,Board.action_size)
			win_probability = float(score) / float(WIN_SCORE)


			player *= -1

			input_boards.append(input_board)
			target_pis.append(action_onehot)
			target_vs.append(win_probability)

			# print("\n")
			# print(parse_encoded_state(input_board))
			# print("best_action " + str(best_action))
		else:
			player == 1
			board = Board() # no valid actions or game ended, reset board
			encoded_state = board.get_encoded_state()

	return input_boards, target_pis, target_vs


#test
# batch = generate_train_batch(NUM_STEPS)
# exit()


# training

g = Game()
n1 = NNet(g)
n1.load_checkpoint('temp',"best.pth.tar")
n1.nnet.model._make_predict_function()

for i in range(NUM_ITERS):
	print("iteration " + str(i) + " / " + str(NUM_ITERS))
	input_boards, target_pis, target_vs = generate_train_batch(NUM_STEPS)
	input_boards = np.asarray(input_boards)
	target_pis = np.asarray(target_pis)
	target_vs = np.asarray(target_vs)

	n1.nnet.model.fit(x = input_boards, y = [target_pis, target_vs], batch_size = int(NUM_STEPS * .6), epochs = 5)

	if i % 5 == 0:
		n1.save_checkpoint('temp',"best.pth.tar")

loss = n1.nnet.model.test_on_batch(x = input_boards, y = [target_pis, target_vs])
print(loss)