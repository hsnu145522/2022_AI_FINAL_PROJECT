import numpy as np
import math
from agent_greedy import greedy
from agent_minimax import minimax
from agent_alphabeta import alphabeta


def find_best_move(board, all_legal_moves, obj_set, player_turn, set_pieces, player1_set, player2_set, player3_set):

    obj_left = [i for i in obj_set + set_pieces if i not in obj_set or i not in set_pieces]
    if len(obj_left) == 2:
        for move in all_legal_moves:
            start_move = move[0]
            end_move = move[1]
            if start_move == obj_left[1] and end_move == obj_left[0]:
                return move
    try:

        if player_turn == 1:
            depth = 2
            score, best_move = alphabeta(board, depth, player_turn, player_turn, player1_set, player2_set,
                                         player3_set, -1000, 1000)#player4_set, player5_set, player6_set, -1000, 1000)
        elif player_turn == 3:
            #depth = 3
            best_move = greedy(board, all_legal_moves, obj_set, player_turn)
            #score, best_move = alphabeta(board, depth, player_turn, player_turn, player1_set, player2_set,player3_set, -1000, 1000)#player4_set, player5_set, player6_set, -1000, 1000)
        #elif player_turn == 5:
        #    depth = 3
        #    score, best_move = alphabeta(board, depth, player_turn, player_turn, player1_set, player2_set,
        #                                 player3_set, player4_set, player5_set, player6_set, -1000, 1000)
        elif player_turn == 2:
            depth = 2
            # score, best_move = minimax(board, depth, player_turn, player_turn, player1_set, player2_set,
            #                            player3_set, player4_set, player5_set, player6_set)
            score, best_move = alphabeta(board, depth, player_turn, player_turn, player1_set, player2_set,
                                         player3_set, -1000, 1000)#player4_set, player5_set, player6_set, -1000, 1000)
        #elif player_turn == 4:
            # depth = 2
            # score, best_move = minimax(board, depth, player_turn, player_turn, player1_set, player2_set,
            #                            player3_set, player4_set, player5_set, player6_set)
        #    best_move = greedy(board, all_legal_moves, obj_set, player_turn)
        #elif player_turn == 6:
        #   best_move = greedy(board, all_legal_moves, obj_set, player_turn)

    except Exception:
        return

    return best_move


def check_win(set_pieces, obj_set):

    for piece in set_pieces:
        if piece not in obj_set:
            return False

    return True
