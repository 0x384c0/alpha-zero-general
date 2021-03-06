import Arena
from MCTS import MCTS

# from tictactoe.TicTacToeGame import TicTacToeGame, display
# from tictactoe.TicTacToePlayers import *
# from tictactoe.keras.NNet import NNetWrapper as NNet


from tk.TKGame import TKGame, display
from tk.TKPlayers import *
from tk.keras.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

# g = TicTacToeGame(3)
g = TKGame()

# all players
rp = RandomPlayer(g).play
hp = HumanTKPlayer(g).play
heurp = HeuristicPlayer().play

# nnet players
n1 = NNet(g)
# n1.load_checkpoint('./pretrained_models/tictactoe/keras/','best.pth.tar')
n1.load_checkpoint('temp/','best.pth.tar')
args1 = dotdict({'numMCTSSims': num_MCTS_sims(), 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

descriptions = {
	rp : "Random Player",
	hp : "Human Player",
	n1p : "NNet Player",
	heurp : "Heuristic Player" 
}
#n2 = NNet(g)
#n2.load_checkpoint('/dev/8x50x25/','best.pth.tar')
#args2 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
#mcts2 = MCTS(g, n2, args2)
#n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))
isPlayWithHuman = os.getenv('PLAY_WITH_HUMAN', "False") == "True"
oppenentOfNN = hp if isPlayWithHuman else rp

arena = Arena.Arena(n1p, oppenentOfNN, g, display=display)
arena.descriptions = descriptions
result = arena.playGames(100, verbose=True)
print("------------------")
print("oneWon ("+ descriptions[n1p] +"):	" + green(result[0]))
print("twoWon:					" + red(result[1]))
print("draw:					" + str(result[2]))
print("------------------")
if mcts1.recursion_errors != 0:
	print("mcts1.recursion_errors " + str(mcts1.recursion_errors))
if mcts1.tree_depth_overflow_errors != 0:
	print("mcts1.tree_depth_overflow_errors " + str(mcts1.tree_depth_overflow_errors))
