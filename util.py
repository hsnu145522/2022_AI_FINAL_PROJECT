import numpy as np
import math

VISITED = 20
NOT_VISITED = 15

### Funcitons for initializeing the board
def build_board():

    board = np.zeros((17, 25)) # the board is 17*25
    # 17 means rows and 25 means columns

    board[:][:] = -1

    # 1
    # set all to player 1
    board[0][12] = 1
    board[1][11] = 1
    board[1][13] = 1
    board[2][10] = 1
    board[2][12] = 1
    board[2][14] = 1
    board[3][9] = 1
    board[3][11] = 1
    board[3][13] = 1
    board[3][15] = 1

    # 2
    board[4][18] = 0
    board[4][20] = 0
    board[4][22] = 0
    board[4][24] = 0
    board[5][19] = 0
    board[5][21] = 0
    board[5][23] = 0
    board[6][20] = 0
    board[6][22] = 0
    board[7][21] = 0

    # 3
    # set all to player 2
    board[9][21] = 2
    board[10][20] = 2
    board[10][22] = 2
    board[11][19] = 2
    board[11][21] = 2
    board[11][23] = 2
    board[12][18] = 2
    board[12][20] = 2
    board[12][22] = 2
    board[12][24] = 2

    # 4
    board[13][9] = 0
    board[13][11] = 0
    board[13][13] = 0
    board[13][15] = 0
    board[14][10] = 0
    board[14][12] = 0
    board[14][14] = 0
    board[15][11] = 0
    board[15][13] = 0
    board[16][12] = 0

    # 5
    # set all to player 3
    board[9][21 - 18] = 3
    board[10][20 - 18] = 3
    board[10][22 - 18] = 3
    board[11][19 - 18] = 3
    board[11][21 - 18] = 3
    board[11][23 - 18] = 3
    board[12][18 - 18] = 3
    board[12][20 - 18] = 3
    board[12][22 - 18] = 3
    board[12][24 - 18] = 3

    # 6
    board[4][18 - 18] = 0
    board[4][20 - 18] = 0
    board[4][22 - 18] = 0
    board[4][24 - 18] = 0
    board[5][19 - 18] = 0
    board[5][21 - 18] = 0
    board[5][23 - 18] = 0
    board[6][20 - 18] = 0
    board[6][22 - 18] = 0
    board[7][21 - 18] = 0

    board[4][8] = 0
    board[4][10] = 0
    board[4][12] = 0
    board[4][14] = 0
    board[4][16] = 0

    board[5][7] = 0
    board[5][9] = 0
    board[5][11] = 0
    board[5][13] = 0
    board[5][15] = 0
    board[5][17] = 0

    board[6][6] = 0
    board[6][8] = 0
    board[6][10] = 0
    board[6][12] = 0
    board[6][14] = 0
    board[6][16] = 0
    board[6][18] = 0

    board[7][5] = 0
    board[7][7] = 0
    board[7][9] = 0
    board[7][11] = 0
    board[7][13] = 0
    board[7][15] = 0
    board[7][17] = 0
    board[7][19] = 0

    board[7][5] = 0
    board[7][7] = 0
    board[7][9] = 0
    board[7][11] = 0
    board[7][13] = 0
    board[7][15] = 0
    board[7][17] = 0
    board[7][19] = 0

    board[8][4] = 0
    board[8][6] = 0
    board[8][8] = 0
    board[8][10] = 0
    board[8][12] = 0
    board[8][14] = 0
    board[8][16] = 0
    board[8][18] = 0
    board[8][20] = 0

    board[9][5] = 0
    board[9][7] = 0
    board[9][9] = 0
    board[9][11] = 0
    board[9][13] = 0
    board[9][15] = 0
    board[9][17] = 0
    board[9][19] = 0

    board[10][6] = 0
    board[10][8] = 0
    board[10][10] = 0
    board[10][12] = 0
    board[10][14] = 0
    board[10][16] = 0
    board[10][18] = 0

    board[11][7] = 0
    board[11][9] = 0
    board[11][11] = 0
    board[11][13] = 0
    board[11][15] = 0
    board[11][17] = 0

    board[12][8] = 0
    board[12][10] = 0
    board[12][12] = 0
    board[12][14] = 0
    board[12][16] = 0

    return board


# build_sets means the start
def build_invalid_set():

    player1_i_set = [[13, 9], [13, 11], [13, 13], [13, 15], [14, 10], [14, 12], [14, 14]]
    player2_i_set = [[4, 4], [4, 6], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]]
    player3_i_set = [[4, 18], [4, 20], [5, 19], [5, 21], [6, 20], [6, 22], [7, 21]]
    #player4_i_set = [[2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]
    #player5_i_set = [[4, 18], [4, 20], [5, 19], [5, 21], [6, 20], [6, 22], [7, 21]]
    #player6_i_set = [[9, 21], [10, 20], [10, 22], [11, 19], [11, 21], [12, 18], [12, 20]]

    return player1_i_set, player2_i_set, player3_i_set# player4_i_set, player5_i_set, player6_i_set


def assign_invalid_set(player_turn, player1_i_set, player2_i_set, player3_i_set):#player4_i_set, player5_i_set,
                       #player6_i_set):

    invalid_set = player1_i_set

    if player_turn == 1:
        invalid_set = player1_i_set
    if player_turn == 2:
        invalid_set = player2_i_set
    if player_turn == 3:
        invalid_set = player3_i_set
    #if player_turn == 4:
    #    invalid_set = player4_i_set
    #if player_turn == 5:
    #    invalid_set = player5_i_set
    #if player_turn == 6:
    #    invalid_set = player6_i_set

    return invalid_set



# build_sets means the start
def build_sets():
    # player 8?
    player1_set = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]
    player2_set = [[9, 21], [10, 20], [10, 22], [11, 19], [11, 21], [11, 23], [12, 18], [12, 20], [12, 22], [12, 24]]
    player3_set = [[9, 3], [10, 2], [10, 4], [11, 1], [11, 3], [11, 5], [12, 0], [12, 2], [12, 4], [12, 6]]
    #player4_set = [[13, 9], [13, 11], [13, 13], [13, 15], [14, 10], [14, 12], [14, 14], [15, 11], [15, 13], [16, 12]]
    #player5_set = [[9, 3], [10, 2], [10, 4], [11, 1], [11, 3], [11, 5], [12, 0], [12, 2], [12, 4], [12, 6]]
    #player6_set = [[4, 0], [4, 2], [4, 4], [4, 6], [5, 1], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]]

    return player1_set, player2_set, player3_set #player4_set, player5_set, player6_set

# build_obj_sets means the goal
def build_obj_sets():

    player1_obj = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 14], [14, 12], [13, 9], [13, 15], [13, 13], [13, 11]]
    player2_obj = [[4, 0], [4, 2], [5, 1], [4, 4], [6, 2], [5, 3], [4, 6], [7, 3], [6, 4], [5, 5]]
    player3_obj = [[4, 24], [5, 23], [4, 22], [6, 22], [4, 20], [5, 21], [7, 21], [4, 18],  [5, 19], [6, 20]]
    #player4_obj = [[0, 12], [1, 13], [1, 11], [2, 14], [2, 10], [2, 12], [3, 15], [3, 9], [3, 11], [3, 13]]
    #player5_obj = [[4, 24], [5, 23], [4, 22], [6, 22], [4, 20], [5, 21], [7, 21], [4, 18],  [5, 19], [6, 20]]
    #player6_obj = [[12, 24], [12, 22], [11, 23], [12, 20], [10, 22], [11, 21], [12, 18], [9, 21], [10, 20], [11, 19]]

    return player1_obj, player2_obj, player3_obj # player4_obj, player5_obj, player6_obj

# build_invalid_homes_sets means the area each player cannot go in
def build_invalid_homes_sets(player1_set, player2_set, player3_set, player1_obj, player2_obj, player3_obj):


    player1_invalid_house = player2_set + player2_obj + player3_set + player3_obj
    player2_invalid_house = player1_set + player1_obj + player3_set + player3_obj
    player3_invalid_house = player2_set + player2_obj + player1_set + player1_obj
    #player4_invalid_house = player5_set + player5_obj + player6_set + player6_obj
    #player5_invalid_house = player4_set + player4_obj + player3_set + player3_obj
    #player6_invalid_house = player4_set + player4_obj + player5_set + player5_obj

    return player1_invalid_house, player2_invalid_house, player3_invalid_house# player4_invalid_house, player5_invalid_house, player6_invalid_house

# assign_set will return the current player's set according to the game order
def assign_set(player_turn, player1_set, player2_set, player3_set):# player4_set, player5_set, player6_set):

    set_player = player1_set

    if player_turn == 1:
        set_player = player1_set
    if player_turn == 2:
        set_player = player2_set
    if player_turn == 3:
        set_player = player3_set
    #if player_turn == 4:
    #    set_player = player4_set
    #if player_turn == 5:
    #    set_player = player5_set
    #if player_turn == 6:
    #    set_player = player6_set

    return set_player

# assign_obj_set will return the current player's goal set according to the game order
def assign_obj_set(player_turn, player1_obj, player2_obj, player3_obj):#player4_obj, player5_obj, player6_obj):

    obj_set = player1_obj

    if player_turn == 1:
        obj_set = player1_obj
    if player_turn == 2:
        obj_set = player2_obj
    if player_turn == 3:
        obj_set = player3_obj
    #if player_turn == 4:
    #    obj_set = player4_obj
    #if player_turn == 5:
    #    obj_set = player5_obj
    #if player_turn == 6:
    #    obj_set = player6_obj

    return obj_set

# assign_invalid_homes_set will return the area current player cannot go in according to the game order
def assign_invalid_homes_set(player_turn, player1_invalid_home, player2_invalid_home, player3_invalid_home):#player4_invalid_home, player5_invalid_home, player6_invalid_home):

    invalid_homes_set = player1_invalid_home

    if player_turn == 1:
        invalid_homes_set = player1_invalid_home
    if player_turn == 2:
        invalid_homes_set = player2_invalid_home
    if player_turn == 3:
        invalid_homes_set = player3_invalid_home
    #if player_turn == 4:
    #    invalid_homes_set = player4_invalid_home
    #if player_turn == 5:
    #    invalid_homes_set = player5_invalid_home
    #if player_turn == 6:
    #    invalid_homes_set = player6_invalid_home

    return invalid_homes_set

# update_player_set is to renew the current player's set
def update_player_set(set_pieces, player_turn, player1_set, player2_set, player3_set):# player4_set, player5_set, player6_set):

    if player_turn == 1:
        player1_set = set_pieces
    if player_turn == 2:
        player2_set = set_pieces
    if player_turn == 3:
        player3_set = set_pieces
    #if player_turn == 4:
    #    player4_set = set_pieces
    #if player_turn == 5:
    #    player5_set = set_pieces
    #if player_turn == 6:
    #    player6_set = set_pieces

    return player1_set, player2_set, player3_set# player4_set, player5_set, player6_set

# check whether the moves are legal
def find_all_legal_moves(board, set_pieces, obj_set, invalid_homes_set):
#def find_all_legal_moves(board, set_pieces, obj_set, invalid_set, invalid_homes_set):

    valid_moves = []

    # this for loop means find all moves (no matter moves is valid or not)
    for piece in set_pieces:

        #if piece not in obj_set:
        color_board = np.full(board.shape, NOT_VISITED)
        valid_moves = check_moves(board, color_board, piece, 0, piece, valid_moves)
        #else:
            #print("- GOAL: piece", piece, "in obj position")

    #print("--- Legal moves:          ", valid_moves)
    #print("----- len", len(valid_moves))
    #print("--- Invalid set:          ", invalid_set)

    #valid_moves = valid_move_in_house(valid_moves, invalid_set, obj_set)
    valid_moves = valid_move_in_house(valid_moves, obj_set)


    #print("--- Legal moves after IS: ", valid_moves)
    #print("----- len", len(valid_moves))

    valid_moves = dont_stop_in_house(valid_moves, invalid_homes_set)

    return valid_moves


def check_moves(board, color_board, start, depth, origin, v_moves):

    [x_v0, y_v0] = start
    color_board[x_v0][y_v0] = VISITED

    neighbors_list = find_neighbors_from(start)

    for x_v1, y_v1 in neighbors_list:

        if depth == 0 and board[x_v1][y_v1] == 0:
            v_moves.append([start, [x_v1, y_v1]])
            # print("nodo origine:", origin, "- profondita:", depth, "- end:", x_v1, y_v1)

        if depth == 0 and board[x_v1][y_v1] > 0:
            x_v2, y_v2 = find_jump_between(start, x_v1, y_v1)
            if board[x_v2][y_v2] == 0:
                v_moves.append([start, [x_v2, y_v2]])
                # print("nodo origine:", origin, "- profondita:", depth, "- start:", start, "- destinazione:", x_v2, y_v2)
                v_moves = check_moves(board, color_board, [x_v2, y_v2], depth + 1, origin, v_moves)

        if depth > 0 and board[x_v1][y_v1] > 0:
            x_v2, y_v2 = find_jump_between(start, x_v1, y_v1)
            if board[x_v2][y_v2] == 0 and color_board[x_v2][y_v2] == NOT_VISITED:
                v_moves.append([origin, [x_v2, y_v2]])
                # print("nodo origine:", origin, "- profondita:", depth, "- start:", start, "- destinazione:", x_v2,
                #       y_v2)
                v_moves = check_moves(board, color_board, [x_v2, y_v2], depth + 1, origin, v_moves)

    return v_moves


def find_neighbors_from(node):

    [x, y] = node

    neighbors_list = []

    nb = [x, y + 2]
    if 0 <= nb[1] <= 24:
        neighbors_list.append([x, y + 2])

    nb = [x, y - 2]
    if 0 <= nb[1] <= 24:
        neighbors_list.append([x, y - 2])

    nb = [x + 1, y + 1]
    if 0 <= nb[0] <= 16 and 0 <= nb[1] <= 24 :
        neighbors_list.append([x + 1, y + 1])

    nb = [x + 1, y - 1]
    if 0 <= nb[0] <= 16 and 0 <= nb[1] <= 24:
        neighbors_list.append([x + 1, y - 1])

    nb = [x - 1, y + 1]
    if 0 <= nb[0] <= 16 and 0 <= nb[1] <= 24:
        neighbors_list.append([x - 1, y + 1])

    nb = [x - 1, y - 1]
    if 0 <= nb[0] <= 16 and 0 <= nb[1] <= 24:
        neighbors_list.append([x - 1, y - 1])

    return neighbors_list


def find_jump_between(start, x_v1, y_v1):

    [start_x, start_y] = start

    x_v2 = x_v1 + (x_v1 - start_x)
    y_v2 = y_v1 + (y_v1 - start_y)

    if 0 <= x_v2 <= 16 and 0 <= y_v2 <= 24:
        return x_v2, y_v2
    else:
        return 0, 0


def valid_move_in_house(valid_moves, obj_set):

    moves_to_remove = []

    for valid_move in valid_moves:

        start_move = valid_move[0]
        end_move = valid_move[1]

        if start_move in obj_set:

            square_start_y = (start_move[1] * 14.43) / 25
            square_end_y = (end_move[1] * 14.43) / 25
            central_pos = (12 * 14.43) / 25

            start_diag = math.sqrt(((8 - start_move[0]) ** 2) + ((central_pos - square_start_y) ** 2))
            end_diag = math.sqrt(((8 - end_move[0]) ** 2) + ((central_pos - square_end_y) ** 2))

            if start_diag > end_diag:
                moves_to_remove.append(valid_move)

    new_valid_moves = [i for i in valid_moves + moves_to_remove if i not in valid_moves or i not in moves_to_remove]

    return new_valid_moves


def dont_stop_in_house(valid_moves, invalid_homes_set):

    moves_to_remove = []

    for valid_move in valid_moves:

        end_move = valid_move[1]

        if end_move in invalid_homes_set:
            moves_to_remove.append(valid_move)

    new_valid_moves = [i for i in valid_moves + moves_to_remove if i not in valid_moves or i not in moves_to_remove]

    return new_valid_moves


def do_move(board, best_move, set_pieces):

    [start_x, start_y] = best_move[0]
    [end_x, end_y] = best_move[1]

    piece = board[start_x][start_y]
    board[start_x][start_y] = 0
    board[end_x][end_y] = piece

    piece_to_remove = [[start_x, start_y]]
    new_set_pieces = [i for i in set_pieces + piece_to_remove if i not in set_pieces or i not in piece_to_remove]

    # set_pieces.remove([start_x, start_y])
    new_set_pieces.append([end_x, end_y])

    return board, new_set_pieces
