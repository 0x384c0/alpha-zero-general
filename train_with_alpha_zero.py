from Coach import Coach
import os
import datetime

# from tictactoe.TicTacToeGame import TicTacToeGame as Game
# from tictactoe.keras.NNet import NNetWrapper as nn

from tk.TKGame import TKGame as Game
from tk.keras.NNet import NNetWrapper as nn

from utils import *

args = dotdict({
    'numIters': number_of_train_iterations(),
    'numEps': 100,
    'tempThreshold': 15,
    'updateThreshold': 0.51,
    'maxlenOfQueue': 200000,
    'numMCTSSims': num_MCTS_sims(),
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
    print(args)
    print("START DATE: " + str(datetime.datetime.now()))

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
    
    print("END DATE: " + str(datetime.datetime.now()))
