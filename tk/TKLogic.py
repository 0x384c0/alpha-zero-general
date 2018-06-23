#! /usr/bin/env python
# -*- coding: utf-8 -*-
from .utils import *
import numpy as np

WIDTH = 9
HEIGHT = 2

INIT_BALLS_COUNT_IN_PIT = 9

MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE = 18 # TODO: find rignt value
BOARD_SIZE =  WIDTH * HEIGHT
WIN_SCORE = (BOARD_SIZE * WIDTH)/HEIGHT - 1


# 0-9 	- player 1
# 10-18 - player -1

class Board():

	shape = (WIDTH * HEIGHT,MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
	action_size = BOARD_SIZE

	def __init__(self):
		self.__size = WIDTH * HEIGHT

		self.__init_state = [INIT_BALLS_COUNT_IN_PIT] * BOARD_SIZE
		self.__players_scores = {
			1	:	0,	# player 1
			-1	:	0	# player -1
		}
		self.__players_tuz = {
			1	:	None,	# player 1
			-1	:	None	# player -1
		}
		self.pieces = data_array_to_one_hot(self.__init_state,MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)




	def __getitem__(self, index): 
		return self.pieces[index]

	def get_legal_moves(self, player):
		return self.__generate_valid_moves(player)

	def has_legal_moves(self):
		return self.__generate_valid_moves(1).count(1) != 0 and self.__generate_valid_moves(-1).count(1) != 0

	def is_win(self, player):
		return self.__players_scores[player] >= WIN_SCORE

	def execute_move(self, move, player):
		game_state = one_hot_batch_to_array(self.pieces)
		balls_in_first_pit = game_state[move]
		last_pit = move + balls_in_first_pit
		last_pit_looped = last_pit if last_pit < len(game_state) 	else last_pit - (len(game_state))
		last_pit_looped -= 1


		if balls_in_first_pit == 1:
			# Если в исходной лунке только один камень, то он перекладывается в следующую лунку.
			last_pit_looped += 1
			game_state[move] = 0
			game_state[last_pit_looped] += balls_in_first_pit
		else:
			# игрок берёт все камни из любой своей лунки «дом» и, начиная с этой же лунки, раскладывает их по одному против часовой стрелки в свои и чужие дома
			game_state[move] = 0
			for pit in range(move,last_pit):
				if pit >= len(game_state):
					pit = pit - len(game_state)
				game_state[pit] += 1


		#Если последний коргоол попадает в дом соперника и 
		#количество коргоолов в нём становится чётным, то коргоолы из этого дома переходят в казан игрока, совершившего ход.
		if  (
			self.__is_pit_dont_belongs_to_player(last_pit_looped,player) and
			game_state[last_pit_looped] % 2 == 0
			):
			self.__players_scores[player] += game_state[last_pit_looped]
			game_state[last_pit_looped] = 0

		opponents_last_pit = WIDTH - 1 if player == 1 else WIDTH / 2 - 1
		if self.__players_tuz[-player] != None:
			opponents_tuz = self.__players_tuz[-player] - WIDTH / 2 if  player == 1 else self.__players_tuz[-player] + WIDTH / 2
		else:
			opponents_tuz = None

		#Если при ходе игрока А последний коргоол попадает в дом игрока Б и в нём после этого оказывается три коргоола, то этот дом объявляется тузом игрока А 
		# 1) игрок не может завести себе туз в самом последнем (девятом) доме соперника,
		# 2) игрок не может завести себе туз в доме с таким же порядковым номером, который имеет лунка-туз соперника,
		# 3) каждый игрок в течение игры может завести себе только один туз.
		if (game_state[last_pit_looped] 	== 3					and 
			move 							!= opponents_last_pit	and
			last_pit_looped 				!= opponents_tuz		and
			self.__players_tuz[player] 		== None):
			#Эти три коргоола попадают в казан игрока
			self.__players_scores[player] += game_state[last_pit_looped]
			game_state[last_pit_looped] = 0
			self.__players_tuz[player] = last_pit_looped
		self.pieces = data_array_to_one_hot(game_state,MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
		return self.pieces

	def __generate_valid_moves(self,player):
		possible_moves = [0] * self.action_size
		game_state = one_hot_batch_to_array(self.pieces)
		for i in range(0,self.action_size):
			if (
				player == 1 and (i < BOARD_SIZE/2) or  #playes 1 side
				player == -1 and (i >= BOARD_SIZE/2)		#playes -1 side
				): 
				possible_moves[i] = 1 if game_state[i] > 0 else 0

		if (self.__players_tuz[player] is not None):
			possible_moves[self.__players_tuz[player]] = 1 if game_state[self.__players_tuz[player]] > 0  else 0
		return possible_moves

	def __is_pit_dont_belongs_to_player(self,pit,player):
		if player == 1:
			players_pit = list(range(0, int(self.__size / 2))) 
		else:
			players_pit = list(range(int(self.__size / 2), self.__size))
		
		if self.__players_tuz[-player] in players_pit:
			players_pit.remove(self.__players_tuz[-player])
		if self.__players_tuz[player] != None:
			players_pit.append(self.__players_tuz[player])
		return pit not in players_pit



#for tests
	def get_player_score(self,player):
		return self.__players_scores[player]

	def set_player_score(self,score,player):
		self.__players_scores[player] = score