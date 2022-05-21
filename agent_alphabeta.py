from util import *
import copy

player1_set, player2_set, player3_set = build_sets()
player1_obj, player2_obj, player3_obj = build_obj_sets()
player1_inv_homes, player2_inv_homes, player3_inv_homes = build_invalid_homes_sets(player1_set, player2_set, player3_set, player1_obj, player2_obj, player3_obj)


def alphabeta(board, depth, player, first_player, player1_set, player2_set, player3_set, alpha, beta):

    board_copy = board[:][:]

    if depth == 0:
        board_score = calculate_board_score(first_player, player1_set, player2_set, player3_set)
        return board_score, None

    set_pieces = assign_set(player, player1_set, player2_set, player3_set)

    obj_set = assign_obj_set(player, player1_obj, player2_obj, player3_obj)

    inv_homes_set = assign_invalid_homes_set(player, player1_inv_homes, player2_inv_homes, player3_inv_homes)
                                             #player4_inv_homes, player5_inv_homes, player6_inv_homes)

    valid_moves = find_all_legal_moves(board_copy, set_pieces, obj_set, inv_homes_set)

    scores = []
    moves = []

    if player == first_player:

        for move in valid_moves:

            board_copy_again = copy.copy(board_copy)
            new_board, new_set_pieces = do_move(board_copy_again, move, set_pieces)

            player1_set, player2_set, player3_set = \
                update_player_set(new_set_pieces, player, player1_set, player2_set, player3_set)

            next_player = player + 1
            if next_player == 4:
                next_player = 1

            score, something = alphabeta(new_board, depth - 1, next_player, first_player, player1_set, player2_set, player3_set, alpha, beta)

            scores.append(score)
            moves.append(move)
            

            alpha = max(score, alpha)
            if beta <= alpha:
                break

        if len(scores) == 0:
            return
        max_score_index = scores.index(max(scores))
        best_move = moves[max_score_index]
        return scores[max_score_index], best_move

    else:

        for move in valid_moves:

            board_copy_again = copy.copy(board_copy)
            new_board, new_set_pieces = do_move(board_copy_again, move, set_pieces)

            player1_set, player2_set, player3_set = \
                update_player_set(new_set_pieces, player, player1_set, player2_set, player3_set)

            next_player = player + 1
            if next_player == 4:
                next_player = 1

            score, something = alphabeta(new_board, depth - 1, next_player, first_player, player1_set, player2_set,
                                         player3_set, alpha, beta)

            scores.append(score)
            moves.append(move)
            

            beta = min(score, beta)
            if beta <= alpha:
                break

        if len(scores) == 0:
            return
        min_score_index = scores.index(min(scores))
        worst_opponent_move = moves[min_score_index]

        return scores[min_score_index], worst_opponent_move


def calculate_board_score(player_turn, p1_pieces, p2_pieces, p3_pieces):

    p1_avg_distance = find_avg_distance(p1_pieces, player1_obj, 16, 12)
    p2_avg_distance = find_avg_distance(p2_pieces, player2_obj, 12, 0)
    p3_avg_distance = find_avg_distance(p3_pieces, player3_obj, 4, 0)

    score = calculate_score(player_turn, p1_avg_distance, p2_avg_distance, p3_avg_distance)

    return score


def find_avg_distance(p_pieces, p_obj, p_default_x, p_default_y):

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


def calculate_score(player_turn, p1_avg_distance, p2_avg_distance, p3_avg_distance):
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



