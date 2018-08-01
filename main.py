from Coach import Coach
import os

# from tictactoe.TicTacToeGame import TicTacToeGame as Game
# from tictactoe.keras.NNet import NNetWrapper as nn

from tk.TKGame import TKGame as Game
from tk.keras.NNet import NNetWrapper as nn

from utils import *

args = dotdict({
    'numIters': 1,#1000,
    'numEps': 100,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 25,
    'arenaCompare': 40,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': True,
    'load_folder_file': ('temp','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})


def is_can_load_checkpoint(args):
    filepath = os.path.join(args.load_folder_file[0], args.load_folder_file[1])
    return os.path.exists(filepath) and args.load_model

if __name__=="__main__":
    # g = Game(3)
    g = Game()
    nnet = nn(g)


    if is_can_load_checkpoint(args):
        print("Load checkpoint from file")
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if is_can_load_checkpoint(args):
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
