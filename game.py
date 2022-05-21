# TODO add player turn in-game
# TODO fix rebuild of interface every damn turn
# TODO won screen + stats
# TODO interface not responding if i dont move cursor on it -> maybe insert FPS?
# TODO reorder functions files

# import numpy as np
import sys
from pygame.locals import *
import pygame as pg
import random
from action import *
from util import *
from gui import Display_surface
from agent import Agent
import argparse


next_move = USEREVENT + 1
restart_game = USEREVENT + 2

class CheckerGame:
    def __init__(self, auto=False):
        self.p1 = Agent(1)
        self.p2 = Agent(2)
        self.p3 = Agent(3)
        self.reset(auto)

    def reset(self, auto):
        self.p1.set, self.p2.set, self.p3.set = build_sets()
        self.p1.obj, self.p2.obj, self.p3.obj = build_obj_sets()
        self.p1.invalid, self.p2.invalid, self.p3.invalid = build_invalid_homes_sets(self.p1.set, self.p2.set, self.p3.set, self.p1.obj, self.p2.obj, self.p3.obj)

        self.board = build_board()
        self.display_surface = Display_surface()

        # player decision
        self.player_turn = random.randint(1, 3)

        # stuck counter
        self.stuck_counter = 0

        # game start
        self.game_over = False
        self.first_turn = True
        self.first_round = True
        self.save_first_p = 100

        self.auto = auto

    def run(self):
        while True:
            #draw_board(self.board, self.display_surface)
            self.display_surface.draw_board(self.board)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == restart_game or (event.type == pg.KEYDOWN and event.key == ord("r")):
                    self.reset(self.auto)
                    event = pg.event.Event(next_move)
                    pg.event.post(event)
                elif ((self.auto and event.type == next_move) or (event.type == pg.KEYDOWN and event.key == ord("a"))) and not self.game_over:
                    # pg.time.wait(100)
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

                    # print("Player", self.player_turn)

                    # consider the pieces of the player of this turn
                    set_pieces = assign_set(self.player_turn, self.p1.set, self.p2.set, self.p3.set)

                    # identify homes of the player of this turn
                    invalid_homes_set = assign_invalid_homes_set(self.player_turn, self.p1.invalid,
                                                                self.p2.invalid, self.p3.invalid)

                    # assign objective set of positions
                    obj_set = assign_obj_set(self.player_turn, self.p1.obj, self.p2.obj, self.p3.obj)

                    # find all legal moves given a piece set of a player
                    all_legal_moves = find_all_legal_moves(self.board, set_pieces, obj_set, invalid_homes_set)

                    # choose the best move
                    if self.first_round:
                        best_move_index = random.randint(0, len(all_legal_moves) - 1)
                        best_move = all_legal_moves[best_move_index]
                    else:
                        best_move = find_best_move(self.board, all_legal_moves, obj_set, self.player_turn, set_pieces,
                                                self.p1.set, self.p2.set, self.p3.set)
                    # print("player:", player_turn, "best move:", best_move)

                    if best_move is None:

                        self.game_over = True
                        self.stuck_counter = self.stuck_counter + 1
                        print('Game stuck counter:', self.stuck_counter)
                        print('[]------------------[]')

                        break

                    # highlight the move chosen
                    self.display_surface.highlight_best_move(best_move)
                    pg.display.update()

                    # do the best move
                    self.board, set_pieces = do_move(self.board, best_move, set_pieces)

                    # update set
                    self.p1.set, self.p2.set, self.p3.set = \
                        update_player_set(set_pieces, self.player_turn, self.p1.set, self.p2.set, self.p3.set)

                    # check if the player has won
                    self.game_over = check_win(set_pieces, obj_set)

                    if self.game_over:
                        if self.player_turn == 1:
                            self.p1.win_cnt += 1
                        if self.player_turn == 2:
                            self.p2.win_cnt += 1
                        if self.player_turn == 3:
                            self.p3.win_cnt += 1

                        total = self.p1.win_cnt + self.p2.win_cnt + self.p3.win_cnt
                        print('Player 1 wins:', self.p1.win_cnt, 'rate:', round(self.p1.win_cnt / total, 3))
                        print('Player 2 wins:', self.p2.win_cnt, 'rate:', round(self.p2.win_cnt / total, 3))
                        print('Player 3 wins:', self.p3.win_cnt, 'rate:', round(self.p3.win_cnt / total, 3))
                        print('total games played:', total)
                        print('[]------------------[]')

                        event = pg.event.Event(restart_game)
                        pg.event.post(event)
                    else:
                        if self.auto:
                            event = pg.event.Event(next_move)
                            pg.event.post(event)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--auto', action='store_true', default=False ,help='run automatically')
    parser.add_argument('-g', '--gui', action='store_true', default=False ,help='show gui')
    args = parser.parse_args()

    game = CheckerGame(args.auto)
    game.run()

