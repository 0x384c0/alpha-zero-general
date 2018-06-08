import numpy as np

WIDTH = 9
HEIGHT = 2

INIT_BALLS_COUNT_IN_PIT = 9

MAX_BALLS_COUNT_IN_PIT = 18 # TODO: find rignt value
BOARD_SIZE =  WIDTH * HEIGHT
WIN_SCORE = (BOARD_SIZE * WIDTH)/HEIGHT - 1


# 0-9 	- player 1
# 10-18 - player -1

def data_array_to_one_hot(array):
	token_ids_one_hot = np.zeros((len(array), MAX_BALLS_COUNT_IN_PIT))
	token_ids_one_hot[np.arange(len(array)), array] = 1
	return token_ids_one_hot

def one_hot_batch_to_array(one_hot_batch):
	array = []
	for one_hot in one_hot_batch:
		array.append(np.argmax(one_hot))
	return array

class Board():

	size = (WIDTH * HEIGHT,MAX_BALLS_COUNT_IN_PIT)
	action_size = BOARD_SIZE# 

	_init_state = [INIT_BALLS_COUNT_IN_PIT] * BOARD_SIZE
	_players_scores = {
		1	:	0,	# player 1
		-1	:	0	# player -1
	}
	_players_tuz = {
		1	:	None,	# player 1
		-1	:	None	# player -1
	}


	def __init__(self):
		self.pieces = data_array_to_one_hot(self._init_state)

	def __getitem__(self, index): 
		return self.pieces[index]

	def get_legal_moves(self, player):
		return self.__generate_valid_moves(player)

	def has_legal_moves(self):
		return self.__generate_valid_moves(1).count(1) != 0 && self.__generate_valid_moves(-1).count(1) != 0

	def is_win(self, player):
		return self._players_scores[player] >= WIN_SCORE

	def execute_move(self, move, player):
		game_state = data_array_to_one_hot(self.pieces)
		balls_in_first_pit = game_state[move]
		last_pit = move + balls_in_first_pit

		#  игрок берёт все камни из любой своей лунки «дом» и, начиная с этой же лунки, раскладывает их по одному против часовой стрелки в свои и чужие дома
		game_state[move] = 0
		for pit in range(move,last_pit): #player 1 TODO: make it for player -1
			game_state[pit] += 1

		#Если последний коргоол попадает в дом соперника и количество коргоолов в нём становится чётным, то коргоолы из этого дома переходят в казан игрока, совершившего ход.
		if game_state[last_pit] % 2 == 0: # TODO:add checking is enemys pit 
			_players_scores[player] += game_state[last_pit]
			game_state[last_pit] = 0

		#Если при ходе игрока А последний коргоол попадает в дом игрока Б и в нём после этого оказывается три коргоола, то этот дом объявляется тузом игрока А 
		# 1) игрок не может завести себе туз в самом последнем (девятом) доме соперника,
		# 2) игрок не может завести себе туз в доме с таким же порядковым номером, который имеет лунка-туз соперника,
		# 3) каждый игрок в течение игры может завести себе только один туз.
		if (game_state[last_pit] == 3 and 
			move < WIDTH - 1 and 
			last_pit != _players_tuz[-player] and 
			_players_tuz[player] != None):
			#Эти три коргоола попадают в казан игрока
			_players_scores[player] += game_state[last_pit]
			game_state[last_pit] = 0
			_players_tuz[player] = last_pit

	def __generate_valid_moves(self,player):
		possible_moves = [0] * action_size
		game_state = data_array_to_one_hot(self.pieces)
		for i in range(0,action_size):
			if (
				player == 1 and (i <= BOARD_SIZE/2) or  #playes 1 side
				player == -1 and (i > BOARD_SIZE/2)		#playes -1 side
				): 
				possible_moves[i] = 1 if game_state[i] > 0 else 0

		if (_players_tuz[player] is not None):
			possible_moves[i] = 1 if game_state[_players_tuz[player]] > 0  else 0









