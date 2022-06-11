import numpy as np
import sys
from pygame.locals import *
import pygame as pg
import random
from board import Board
from util import *
from gui import Display_surface
from agents import GreedyAgent
from agents import AlphaBetaAgent
from agents import AlphaBetaTTAgent
import argparse
import time
import copy


next_move = USEREVENT + 1

class CheckerGame:
    def __init__(self, auto=False, gui=False, seed=100):
        self.p1 = AlphaBetaAgent(depth=3)
        self.p1_2 = AlphaBetaTTAgent(depth=3)
        self.p2 = AlphaBetaAgent(depth=2)
        self.p3 = GreedyAgent()
        self.p1.obj, self.p2.obj, self.p3.obj = build_obj_sets()
        self.total = 0
        self.auto = auto
        self.gui = gui
        self.p1_time_compare = [0, 0]

        self.p1_2.obj = self.p1.obj
        #self.p1_2.obj = copy.copy(self.p1.obj)

        random.seed(seed)
        np.random.seed(seed)

        self.reset()

    def reset(self):
        self.p1.set, self.p2.set, self.p3.set = build_sets()
        self.p1.invalid, self.p2.invalid, self.p3.invalid = build_invalid_homes_sets(self.p1.set, self.p2.set, self.p3.set, self.p1.obj, self.p2.obj, self.p3.obj)

        self.p1_2.set = self.p1.set
        self.p1_2.invalid = self.p1.invalid
        #self.p1_2.set = copy.copy(self.p1.set)
        #self.p1_2.invalid = copy.copy(self.p1.invalid)

        # self.board = build_board()
        self.board = Board()

        self.display_surface = Display_surface(self.gui)

        # player decision
        self.player_turn = random.randint(1, 3)

        # stuck counter
        self.stuck_counter = 0

        # game start
        self.game_over = False
        self.first_turn = True
        self.first_round = True
        self.save_first_p = 100

        self.p1_time_compare = [0, 0]

        event = pg.event.Event(next_move)
        pg.event.post(event)

        return self.board.board


    def check_win(self, set_pieces, obj_set):

        for piece in set_pieces:
            if piece not in obj_set:
                return False
        return True

    def choose_action(self, legal_moves):
        
        if self.player_turn == 1: # compare
            # AlphaBeta ============================================
            start = time.time() 
            action_alphaBeta = self.p1.choose_action(self.board.board, self.player_turn, self.player_turn, self.p1.set, self.p2.set, self.p3.set, -1000, 1000)
            end = time.time()
            self.p1_time_compare[0] += end - start
            # =======================================================

            # AlphaBetaTT ============================================
            start = time.time()
            action_alphaBetaTT = self.p1_2.choose_action(self.board, self.player_turn, self.player_turn, self.p1.set, self.p2.set, self.p3.set, -1000, 1000)
            end = time.time()
            self.p1_time_compare[1] += end - start
            # =======================================================

            if action_alphaBetaTT[0] not in self.p1_2.set:
                print(action_alphaBetaTT)
                print("Error")
                exit()
            print(action_alphaBetaTT)
            print("p1.set", self.p1.set)
            print("p1_2.set", self.p1_2.set)

            print("alphaBeta:", action_alphaBeta, "TT:", action_alphaBetaTT)
            for _action in action_alphaBeta:
                if _action not in action_alphaBetaTT:
                    print("Error: alphaBeta and alphaBetaTT are not the same.")
                    break

            action = action_alphaBetaTT
        elif self.player_turn == 2: # AlphaBeta
            action =  self.p2.choose_action(self.board.board, self.player_turn, self.player_turn, self.p1.set, self.p2.set, self.p3.set, -1000, 1000)
        elif self.player_turn == 3: # Greedy
            action = self.p3.choose_action(self.board.board, legal_moves)
        
        return action

    def run(self):
        while True:
            if self.gui:
                self.display_surface.draw_board(self.board.board)
            for event in pg.event.get():
                if event.type == QUIT or (event.type == pg.KEYDOWN and event.key == ord("q")):
                    pg.quit()
                    sys.exit()

                elif event.type == pg.KEYDOWN and event.key == ord("r"):
                    self.reset()

                elif not self.game_over and (event.type == next_move or (event.type == pg.KEYDOWN and event.key == ord("a"))):
                    # change player turn
                    self.player_turn += 1
                    if self.player_turn == 4:
                        self.player_turn = 1

                    # randomize first move
                    if self.player_turn == self.save_first_p:
                        self.first_round = False
                    if self.first_turn:
                        self.save_first_p = self.player_turn
                        self.first_turn = False

                    # consider the pieces of the player of this turn
                    set_pieces = assign_set(self.player_turn, self.p1.set, self.p2.set, self.p3.set)
                    # identify homes of the player of this turn
                    invalid_homes_set = assign_invalid_homes_set(self.player_turn, self.p1.invalid, self.p2.invalid, self.p3.invalid)
                    # assign objective set of positions
                    obj_set = assign_obj_set(self.player_turn, self.p1.obj, self.p2.obj, self.p3.obj)
                    # find all legal moves given a piece set of a player
                    all_legal_moves = find_all_legal_moves(self.board.board, set_pieces, obj_set, invalid_homes_set)

                    # copy
                    self.p1_2.set = self.p1.set

                    # last step
                    last_pair = [i for i in set_pieces + obj_set if i not in set_pieces or i not in obj_set]

                    # choose the best move
                    if self.first_round:
                        best_move_index = random.randint(0, len(all_legal_moves) - 1)
                        best_move = all_legal_moves[best_move_index]

                    elif len(last_pair) == 2:
                        best_move = None
                        for start, end in all_legal_moves:
                            if start == last_pair[0] and end == last_pair[1]:
                                best_move = [start, end]
                        if best_move is None:
                            best_move = self.choose_action(all_legal_moves)
                    else:
                        best_move = self.choose_action(all_legal_moves)
                        
                    if best_move is None:
                        self.game_over = True
                        self.stuck_counter = self.stuck_counter + 1
                        print('Game stuck counter:', self.stuck_counter)
                        print('[]------------------[]')
                        break

                    self.board.updateHashKey(self.player_turn, best_move)

                    # highlight the move chosen
                    if self.gui:
                        self.display_surface.highlight_best_move(best_move)
                        pg.display.update()

                    # do the best move
                    self.board.board, set_pieces = do_move(self.board.board, best_move, set_pieces)

                    # update set
                    self.p1.set, self.p2.set, self.p3.set = \
                        update_player_set(set_pieces, self.player_turn, self.p1.set, self.p2.set, self.p3.set)

                    # check if the player has won
                    self.game_over = self.check_win(set_pieces, obj_set)

                    if self.game_over:
                        if self.player_turn == 1:
                            self.p1.win_cnt += 1
                        elif self.player_turn == 2:
                            self.p2.win_cnt += 1
                        elif self.player_turn == 3:
                            self.p3.win_cnt += 1

                        self.total += 1
                        print('Player 1(R) wins:', self.p1.win_cnt, f'({round(100 * self.p1.win_cnt / self.total, 3)}%)')
                        print('Player 2(G) wins:', self.p2.win_cnt, f'({round(100 * self.p2.win_cnt / self.total, 3)}%)')
                        print('Player 3(Y) wins:', self.p3.win_cnt, f'({round(100 * self.p3.win_cnt / self.total, 3)}%)')
                        print('total games played:', self.total)

                        print('time_alphabeta:', self.p1_time_compare[0])
                        print('time_alphabetaTT:', self.p1_time_compare[1])
                        print('[]------------------[]')

                        self.reset()

                    elif self.auto:
                        event = pg.event.Event(next_move)
                        pg.event.post(event)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--auto', action='store_true', default=False ,help='run automatically')
    parser.add_argument('-g', '--gui', action='store_true', default=False ,help='show gui')
    args = parser.parse_args()

    game = CheckerGame(args.auto, args.gui)
    game.run()

