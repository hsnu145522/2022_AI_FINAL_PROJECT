import math
from util import *
import copy
from board import *
import time
import random

class Agent:
    def __init__(self):
        self.win_cnt = 0
        self.set = []
        self.obj = []
        self.invalid = []
        self.visited_node = 0

    def evaluation(self, board, piece_set):
        obj_available = []

        for pos in self.obj:
            if board[tuple(pos)] == 0:
                obj_available.append(pos)
        
        distance = 0
        if len(obj_available) == 0:
            return 0
        # obj = np.average(obj_available, axis=0)
        obj = obj_available[0]
        for piece in piece_set:
            x, y = piece
            obj_x, obj_y = obj
            y = (y * 14.43) / 25
            obj_y = (obj_y * 14.43) / 25

            distance += math.sqrt((x - obj_x)**2 + (y - obj_y)**2) ** 1.5

        score = -distance
        return score


class GreedyAgent(Agent):
    def __init__(self):
        super().__init__()

    def choose_action(self, board, legal_moves):
        start = time.time()
        obj_available = []

        for pos in self.obj:
            if board[tuple(pos)] == 0:
                obj_available.append(pos)

        best_move = 0
        move_index = 0
        max_score = float('-inf')
        for move in legal_moves:
            start = move[0]
            end = move[1]

            self.set.remove(start)
            self.set.append(end)
            board[tuple(end)] = board[tuple(start)]
            board[tuple(start)] = 0
            
            score = self.evaluation(board, self.set)

            self.set.remove(end)
            self.set.append(start)
            board[tuple(start)] = board[tuple(end)]
            board[tuple(end)] = 0

            if score > max_score:
                max_score = score
                best_move = move_index

            move_index += 1
            

        # max_distance_metric = 0
        # move_index = 0
        # best_move = 0

        # for move in legal_moves:

        #     [start_x, start_y] = move[0]
        #     [end_x, end_y] = move[1]

        #     for obj in obj_available:

        #         [obj_x, obj_y] = obj

        #         square_start_y = (start_y * 14.43) / 25 
        #         square_end_y = (end_y * 14.43) / 25
        #         square_obj_y = (obj_y * 14.43) / 25

        #         start_diag = math.sqrt(((obj_x - start_x) ** 2) + ((square_obj_y - square_start_y) ** 2))
        #         end_diag = math.sqrt(((obj_x - end_x) ** 2) + ((square_obj_y - square_end_y) ** 2))

        #         distance_travel = start_diag - end_diag
        #         distance_metric = distance_travel + start_diag * 0.5

        #         if distance_metric > max_distance_metric:
        #             best_move = move_index
        #             max_distance_metric = distance_metric

        #     move_index = move_index + 1
        return legal_moves[best_move]



player1_set, player2_set, player3_set = build_sets()
player1_obj, player2_obj, player3_obj = build_obj_sets()
player1_inv_homes, player2_inv_homes, player3_inv_homes = build_invalid_homes_sets(player1_set, player2_set, player3_set, player1_obj, player2_obj, player3_obj)
class AlphaBetaAgent(Agent):
    def __init__(self, depth=1):
        super().__init__()
        self.depth = depth

    def choose_action(self, board, player, first_player, player1_set, player2_set, player3_set, alpha, beta, end):
        _, action = self.alphabeta(board, self.depth, player, first_player, player1_set, player2_set, player3_set, alpha, beta, end)
        return action

    def alphabeta(self, board, depth, player, first_player, player1_set, player2_set, player3_set, alpha, beta, end):
        self.visited_node += 1

        current_board = board[:][:]

        set_pieces = assign_set(player, player1_set, player2_set, player3_set)
        obj_set = assign_obj_set(player, player1_obj, player2_obj, player3_obj)
        inv_homes_set = assign_invalid_homes_set(player, player1_inv_homes, player2_inv_homes, player3_inv_homes)

        if depth == 0:
            # board_score = self.calculate_board_score(first_player, player1_set, player2_set, player3_set)
            if first_player == 1:
                board_score = self.evaluation(current_board, player1_set)
            elif first_player == 2:
                board_score = self.evaluation(current_board, player2_set)
            else:
                board_score = self.evaluation(current_board, player3_set)
            return board_score, None

        
                                                

        valid_moves = find_all_legal_moves(current_board, set_pieces, obj_set, inv_homes_set)

        scores = []
        moves = []

        if player == first_player:

            for move in valid_moves:

                current_board_copy = copy.copy(current_board)
                new_board, new_set_pieces = do_move(current_board_copy, move, set_pieces)

                player1_set, player2_set, player3_set = \
                    update_player_set(new_set_pieces, player, player1_set, player2_set, player3_set)

                next_player = player + 1
                if next_player == 4:
                    next_player = 1
                while end[next_player-1]:
                    next_player += 1
                    if next_player == 4:
                        next_player = 1

                score, useless_move = self.alphabeta(new_board, depth - 1, next_player, first_player, player1_set, player2_set, player3_set, alpha, beta,end)

                scores.append(score)
                moves.append(move)
                

                alpha = max(score, alpha)
                if beta <= alpha:
                    break

            if len(scores) == 0:
                return 0, None
                
            max_score_index = scores.index(max(scores))
            best_move = moves[max_score_index]
            return scores[max_score_index], best_move

        else:

            for move in valid_moves:

                current_board_copy = copy.copy(current_board)
                new_board, new_set_pieces = do_move(current_board_copy, move, set_pieces)

                player1_set, player2_set, player3_set = \
                    update_player_set(new_set_pieces, player, player1_set, player2_set, player3_set)

                next_player = player + 1
                if next_player == 4:
                    next_player = 1
                while end[next_player-1]:
                    next_player = next_player + 1
                    if next_player == 4:
                        next_player = 1


                score, useless_move = self.alphabeta(new_board, depth - 1, next_player, first_player, player1_set, player2_set, player3_set, alpha, beta,end)

                scores.append(score)
                moves.append(move)
                

                beta = min(score, beta)
                if beta <= alpha:
                    break

            if len(scores) == 0:
                return 0, None
            min_score_index = scores.index(min(scores))
            worst_opponent_move = moves[min_score_index]

            return scores[min_score_index], worst_opponent_move


    def calculate_board_score(self, player_turn, p1_pieces, p2_pieces, p3_pieces):

        p1_avg_distance = self.find_avg_distance(p1_pieces, player1_obj, 16, 12)
        p2_avg_distance = self.find_avg_distance(p2_pieces, player2_obj, 12, 0)
        p3_avg_distance = self.find_avg_distance(p3_pieces, player3_obj, 4, 0)

        score = self.calculate_score(player_turn, p1_avg_distance, p2_avg_distance, p3_avg_distance)

        return score


    def find_avg_distance(self, p_pieces, p_obj, p_default_x, p_default_y):

        total_distance = 0
        obj_x = p_default_x
        obj_y = p_default_y
        for obj_piece in p_obj:
            if obj_piece not in p_pieces:
                [obj_x, obj_y] = obj_piece
                break

        for piece in p_pieces:

            [x, y] = piece

            square_y = (y * 14.43) / 25
            square_obj_y = (obj_y * 14.43) / 25

            distance_diag = math.sqrt(((obj_x - x) ** 2) + ((square_obj_y - square_y) ** 2))

            total_distance = total_distance + distance_diag

        avg_distance = total_distance / 10

        return avg_distance


    def calculate_score(self, player_turn, p1_avg_distance, p2_avg_distance, p3_avg_distance):
        score = 0

        if player_turn == 1:
            # print("-- loop player 1")
            pturn_avg_distance = p1_avg_distance
            score = ((p2_avg_distance - pturn_avg_distance) +
                    (p3_avg_distance - pturn_avg_distance)) / 2
        elif player_turn == 2:
            # print("-- loop player 2")
            pturn_avg_distance = p2_avg_distance
            score = ((p1_avg_distance - pturn_avg_distance) +
                    (p3_avg_distance - pturn_avg_distance)) / 2
        elif player_turn == 3:
            # print("-- loop player 3")
            pturn_avg_distance = p3_avg_distance
            score = ((p2_avg_distance - pturn_avg_distance) +
                    (p1_avg_distance - pturn_avg_distance)) / 2
        
        return score


LOWERBOUND = 0
UPPERBOUND = 1
EXACT = 2
class TTEntry():
    def __init__(self):
        self.type = EXACT
        self.value = 0
        self.depth = 0

class AlphaBetaTTAgent(AlphaBetaAgent):
    def __init__(self, depth=1):
        super().__init__()
        self.depth = depth
        self.transposition_table = [None for _ in range(1000000)] 
    
    def getTTEntry(self, key):
        return self.transposition_table[key % len(self.transposition_table)]
    
    def storeTTEntry(self, key, value, _type, depth):
        tte = self.getTTEntry(key)
        if tte is None:
            tte = TTEntry()
        tte.value = value
        tte.type = _type    
        tte.depth = depth
        self.transposition_table[key % len(self.transposition_table)] = tte

    # def choose_action(self, board, player, first_player, player1_set, player2_set, player3_set, alpha, beta,end):
    #     _, action = self.alphabeta(board, self.depth, player, first_player, player1_set, player2_set, player3_set, alpha, beta,end)
    #     return action

    def alphabeta(self, board, depth, player, first_player, player1_set, player2_set, player3_set, alpha, beta,end):
        self.visited_node += 1

        current_board = copy.copy(board)
        current_board.board = copy.copy(board.board)

        tte = self.getTTEntry(board.getHashKey())


        flag_tte = False
        flag_depth_0 = False

        if tte != None and tte.depth >= depth:
            if tte.type == EXACT:
                flag_tte = True
                #return tte.value, valid_moves[random.randint(0, len(valid_moves) - 1)]

            if tte.type == LOWERBOUND and tte.value > alpha:
                alpha = tte.value
            elif tte.type == UPPERBOUND and tte.value < beta:
                beta = tte.value

            if alpha >= beta:
                flag_tte = True
                #return tte.value, valid_moves[random.randint(0, len(valid_moves) - 1)]

        set_pieces = assign_set(player, player1_set, player2_set, player3_set)

        obj_set = assign_obj_set(player, player1_obj, player2_obj, player3_obj)

        inv_homes_set = assign_invalid_homes_set(player, player1_inv_homes, player2_inv_homes, player3_inv_homes)

        valid_moves = find_all_legal_moves(current_board.board, set_pieces, obj_set, inv_homes_set)   
        #print(len(valid_moves))
        if depth == 0:
            # board_score = self.calculate_board_score(first_player, player1_set, player2_set, player3_set)
            # board_score = self.evaluation(current_board.board, set_pieces)
            if first_player == 1:
                board_score = self.evaluation(current_board.board, player1_set)
            elif first_player == 2:
                board_score = self.evaluation(current_board.board, player2_set)
            else:
                board_score = self.evaluation(current_board.board, player3_set)

            if board_score <= alpha:
                self.storeTTEntry(board.getHashKey(), board_score, LOWERBOUND, depth)
            elif board_score >= beta:
                self.storeTTEntry(board.getHashKey(), board_score, UPPERBOUND, depth)
            else:
                self.storeTTEntry(board.getHashKey(), board_score, EXACT, depth)
            
            flag_depth_0 = True
            

        # if end[player-1]:
        #     return board_score, None
        if len(valid_moves)==0:
            print("Warning: valid_moves is empty")
            return 0, None
        #print("valid_moves: ",len(valid_moves))
        if flag_tte:
            return tte.value, valid_moves[random.randint(0, len(valid_moves) - 1)]
        if flag_depth_0:
            return board_score, valid_moves[random.randint(0, len(valid_moves) - 1)] 

        scores = []
        moves = []

        if player == first_player:

            for move in valid_moves:

                current_board_copy = copy.copy(current_board)
                current_board_copy.board = copy.copy(current_board.board)

                current_board_copy.board, new_set_pieces = do_move(current_board_copy.board, move, set_pieces)
                current_board_copy.updateHashKey(player, move)

                player1_set, player2_set, player3_set = \
                    update_player_set(new_set_pieces, player, player1_set, player2_set, player3_set)

                next_player = player + 1
                if next_player == 4:
                    next_player = 1
                while end[next_player-1]:
                    next_player += 1
                    if next_player == 4:
                        next_player = 1 


                score, useless_move = self.alphabeta(current_board_copy, depth - 1, next_player, first_player, player1_set, player2_set, player3_set, alpha, beta,end)

                scores.append(score)
                moves.append(move)
                

                alpha = max(score, alpha)
                if beta <= alpha:
                    break

            if len(scores) == 0:
                return
            max_score_index = scores.index(max(scores))
            best_move = moves[max_score_index]


            if scores[max_score_index] <= alpha:
                self.storeTTEntry(board.getHashKey(), scores[max_score_index], LOWERBOUND, depth)
            if scores[max_score_index] >= beta:
                self.storeTTEntry(board.getHashKey(), scores[max_score_index], UPPERBOUND, depth)
            else:
                self.storeTTEntry(board.getHashKey(), scores[max_score_index], EXACT, depth)
            
            return scores[max_score_index], best_move

        else:

            for move in valid_moves:

                current_board_copy = copy.copy(current_board)
                current_board_copy.board = copy.copy(current_board.board)

                current_board_copy.board, new_set_pieces = do_move(current_board_copy.board, move, set_pieces)
                current_board_copy.updateHashKey(player, move)

                player1_set, player2_set, player3_set = \
                    update_player_set(new_set_pieces, player, player1_set, player2_set, player3_set)

                next_player = player + 1
                if next_player == 4:
                    next_player = 1
                while end[next_player-1]:
                    next_player += 1
                    if next_player == 4:
                        next_player = 1  

                score, useless_move = self.alphabeta(current_board_copy, depth - 1, next_player, first_player, player1_set, player2_set, player3_set, alpha, beta,end)

                scores.append(score)
                moves.append(move)

                beta = min(score, beta)
                if beta <= alpha:
                    break

            if len(scores) == 0:
                return
            min_score_index = scores.index(min(scores))
            worst_opponent_move = moves[min_score_index]

            if scores[min_score_index] <= alpha:
                self.storeTTEntry(current_board.getHashKey(), scores[min_score_index], LOWERBOUND, depth)
            elif scores[min_score_index] >= beta:
                self.storeTTEntry(current_board.getHashKey(), scores[min_score_index], UPPERBOUND, depth)
            else:
                self.storeTTEntry(current_board.getHashKey(), scores[min_score_index], EXACT, depth)
            
            return scores[min_score_index], worst_opponent_move


    # def calculate_board_score(self, player_turn, p1_pieces, p2_pieces, p3_pieces):

    #     p1_avg_distance = self.find_avg_distance(p1_pieces, player1_obj, 16, 12)
    #     p2_avg_distance = self.find_avg_distance(p2_pieces, player2_obj, 12, 0)
    #     p3_avg_distance = self.find_avg_distance(p3_pieces, player3_obj, 4, 0)

    #     score = self.calculate_score(player_turn, p1_avg_distance, p2_avg_distance, p3_avg_distance)

    #     return score


    # def find_avg_distance(self, p_pieces, p_obj, p_default_x, p_default_y):

    #     total_distance = 0
    #     obj_x = p_default_x
    #     obj_y = p_default_y
    #     for obj_piece in p_obj:
    #         if obj_piece not in p_pieces:
    #             [obj_x, obj_y] = obj_piece
    #             break

    #     for piece in p_pieces:

    #         [x, y] = piece

    #         square_y = (y * 14.43) / 25
    #         square_obj_y = (obj_y * 14.43) / 25

    #         distance_diag = math.sqrt(((obj_x - x) ** 2) + ((square_obj_y - square_y) ** 2))

    #         total_distance = total_distance + distance_diag

    #     avg_distance = total_distance / 10

    #     return avg_distance


    # def calculate_score(self, player_turn, p1_avg_distance, p2_avg_distance, p3_avg_distance):
    #     score = 0

    #     if player_turn == 1:
    #         # print("-- loop player 1")
    #         pturn_avg_distance = p1_avg_distance
    #         score = ((p2_avg_distance - pturn_avg_distance) +
    #                 (p3_avg_distance - pturn_avg_distance)) / 2
    #     elif player_turn == 2:
    #         # print("-- loop player 2")
    #         pturn_avg_distance = p2_avg_distance
    #         score = ((p1_avg_distance - pturn_avg_distance) +
    #                 (p3_avg_distance - pturn_avg_distance)) / 2
    #     elif player_turn == 3:
    #         # print("-- loop player 3")
    #         pturn_avg_distance = p3_avg_distance
    #         score = ((p2_avg_distance - pturn_avg_distance) +
    #                 (p1_avg_distance - pturn_avg_distance)) / 2
        
    #     return score
