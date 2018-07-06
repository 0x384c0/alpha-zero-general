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
# hp = HumanTicTacToePlayer(g).play
hp = HumanTKPlayer(g).play

# nnet players
n1 = NNet(g)
# n1.load_checkpoint('./pretrained_models/tictactoe/keras/','best.pth.tar')
n1.load_checkpoint('temp/','best.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))


#n2 = NNet(g)
#n2.load_checkpoint('/dev/8x50x25/','best.pth.tar')
#args2 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
#mcts2 = MCTS(g, n2, args2)
#n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

arena = Arena.Arena(n1p, rp, g, display=display)
result = arena.playGames(4, verbose=True)
print("oneWon: " + str(result[0]) + " twoWon (neural network): " + str(result[1]) + " draw: " + str(result[2]))
