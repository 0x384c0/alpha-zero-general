import numpy as np
from pytorch_classification.utils import Bar, AverageMeter
import time
from utils import *

class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """
    def __init__(self, player1, player2, game, display=None):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.

        see othello/OthelloPlayers.py for an example. See pit.py for pitting
        human players/other baselines with each other.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

    def playGame(self, verbose=False):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player2, None, self.player1]
        curPlayer = 1
        board = self.game.getInitBoard()
        it = 0
        while self.game.getGameEnded(board, curPlayer)==0:
            it+=1

            if it > max_num_of_steps():
                print("\nArena it > max_num_of_steps()")
                break

            if verbose:
                assert(self.display)
                player_descr = green("\tPlayer " + str(curPlayer)) if curPlayer == 1 else red("Player " + str(curPlayer))
                if self.descriptions != None:
                    player_descr += "\t" + self.descriptions[players[curPlayer+1]]
                print("\n --- Turn " + str(it) + " " + player_descr)
                self.display(board)


            canonical_form = self.game.getCanonicalForm(board, curPlayer)

            action = players[curPlayer+1](canonical_form)
            valids = self.game.getValidMoves(canonical_form,1)


            if is_debug_mode():
                print("taken action: " + bpurple(action) + "\t of valid actions: " + str(valids))

            if valids[action]==0:
                print(red("WARNING - Arena.playGame invalid action"))
                print("valids")
                print(valids)
                print("len(valids)")
                print(len(valids))
                print("action")
                print(action)
                if is_debug_mode():
                    assert valids[action] > 0
                else:
                    action = valids.tolist().index(1)


            board, curPlayer = self.game.getNextState(board, curPlayer, action)
        
        if it > max_num_of_steps():
            if self.display != None:
                self.display(board)
            print("WARNING: Game over with step overflow: Turn " + str(it) + " Result " + str(self.game.getGameEnded(board, 1)) + "\n------------------------------\n")
            return step_overflow_penalty()

        if verbose:
            if self.display != None:
                self.display(board)
            print("Game over: Turn " + str(it) + " Result " + str(self.game.getGameEnded(board, 1)) + "\n------------------------------\n")
        return self.game.getGameEnded(board, 1)

    def playGames(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.

        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
            draws:  games won by nobody
        """
        eps_time = AverageMeter()
        bar = Bar('Arena.playGames', max=num)
        end = time.time()
        eps = 0
        maxeps = int(num)

        num = int(num/2)
        oneWon = 0
        twoWon = 0
        draws = 0
        for _ in range(num):
            gameResult = self.playGame(verbose=verbose)
            if gameResult==1:
                oneWon+=1
            elif gameResult==-1:
                twoWon+=1
            else:
                draws+=1
            # bookkeeping + plot progress
            eps += 1
            eps_time.update(time.time() - end)
            end = time.time()
            bar.suffix  = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(eps=eps+1, maxeps=maxeps, et=eps_time.avg,
                                                                                                       total=bar.elapsed_td, eta=bar.eta_td)
            bar.next()

        self.player1, self.player2 = self.player2, self.player1
        
        for _ in range(num):
            gameResult = self.playGame(verbose=verbose)
            if gameResult==-1:
                oneWon+=1                
            elif gameResult==1:
                twoWon+=1
            else:
                draws+=1
            # bookkeeping + plot progress
            eps += 1
            eps_time.update(time.time() - end)
            end = time.time()
            bar.suffix  = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(eps=eps+1, maxeps=num, et=eps_time.avg,
                                                                                                       total=bar.elapsed_td, eta=bar.eta_td)
            bar.next()
            
        bar.finish()

        return oneWon, twoWon, draws
