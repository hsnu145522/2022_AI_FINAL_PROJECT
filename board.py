import numpy as np

class Board:
    def __init__(self):
        self.board = self.build_board()
    def build_board(self):
        self.board = np.zeros((17, 25)) # the board is 17*25
        # 17 means rows and 25 means columns
        self.board[:][:] = -1
        # 1
        # set all to player 1
        self.board[0][12] = 1
        self.board[1][11] = 1
        self.board[1][13] = 1
        self.board[2][10] = 1
        self.board[2][12] = 1
        self.board[2][14] = 1
        self.board[3][9] = 1
        self.board[3][11] = 1
        self.board[3][13] = 1
        self.board[3][15] = 1

        # 2
        self.board[4][18] = 0
        self.board[4][20] = 0
        self.board[4][22] = 0
        self.board[4][24] = 0
        self.board[5][19] = 0
        self.board[5][21] = 0
        self.board[5][23] = 0
        self.board[6][20] = 0
        self.board[6][22] = 0
        self.board[7][21] = 0

        # 3
        # set all to player 2
        self.board[9][21] = 2
        self.board[10][20] = 2
        self.board[10][22] = 2
        self.board[11][19] = 2
        self.board[11][21] = 2
        self.board[11][23] = 2
        self.board[12][18] = 2
        self.board[12][20] = 2
        self.board[12][22] = 2
        self.board[12][24] = 2

        # 4
        self.board[13][9] = 0
        self.board[13][11] = 0
        self.board[13][13] = 0
        self.board[13][15] = 0
        self.board[14][10] = 0
        self.board[14][12] = 0
        self.board[14][14] = 0
        self.board[15][11] = 0
        self.board[15][13] = 0
        self.board[16][12] = 0

        # 5
        # set all to player 3
        self.board[9][21 - 18] = 3
        self.board[10][20 - 18] = 3
        self.board[10][22 - 18] = 3
        self.board[11][19 - 18] = 3
        self.board[11][21 - 18] = 3
        self.board[11][23 - 18] = 3
        self.board[12][18 - 18] = 3
        self.board[12][20 - 18] = 3
        self.board[12][22 - 18] = 3
        self.board[12][24 - 18] = 3

        # 6
        self.board[4][18 - 18] = 0
        self.board[4][20 - 18] = 0
        self.board[4][22 - 18] = 0
        self.board[4][24 - 18] = 0
        self.board[5][19 - 18] = 0
        self.board[5][21 - 18] = 0
        self.board[5][23 - 18] = 0
        self.board[6][20 - 18] = 0
        self.board[6][22 - 18] = 0
        self.board[7][21 - 18] = 0

        self.board[4][8] = 0
        self.board[4][10] = 0
        self.board[4][12] = 0
        self.board[4][14] = 0
        self.board[4][16] = 0

        self.board[5][7] = 0
        self.board[5][9] = 0
        self.board[5][11] = 0
        self.board[5][13] = 0
        self.board[5][15] = 0
        self.board[5][17] = 0

        self.board[6][6] = 0
        self.board[6][8] = 0
        self.board[6][10] = 0
        self.board[6][12] = 0
        self.board[6][14] = 0
        self.board[6][16] = 0
        self.board[6][18] = 0

        self.board[7][5] = 0
        self.board[7][7] = 0
        self.board[7][9] = 0
        self.board[7][11] = 0
        self.board[7][13] = 0
        self.board[7][15] = 0
        self.board[7][17] = 0
        self.board[7][19] = 0

        self.board[7][5] = 0
        self.board[7][7] = 0
        self.board[7][9] = 0
        self.board[7][11] = 0
        self.board[7][13] = 0
        self.board[7][15] = 0
        self.board[7][17] = 0
        self.board[7][19] = 0

        self.board[8][4] = 0
        self.board[8][6] = 0
        self.board[8][8] = 0
        self.board[8][10] = 0
        self.board[8][12] = 0
        self.board[8][14] = 0
        self.board[8][16] = 0
        self.board[8][18] = 0
        self.board[8][20] = 0

        self.board[9][5] = 0
        self.board[9][7] = 0
        self.board[9][9] = 0
        self.board[9][11] = 0
        self.board[9][13] = 0
        self.board[9][15] = 0
        self.board[9][17] = 0
        self.board[9][19] = 0

        self.board[10][6] = 0
        self.board[10][8] = 0
        self.board[10][10] = 0
        self.board[10][12] = 0
        self.board[10][14] = 0
        self.board[10][16] = 0
        self.board[10][18] = 0

        self.board[11][7] = 0
        self.board[11][9] = 0
        self.board[11][11] = 0
        self.board[11][13] = 0
        self.board[11][15] = 0
        self.board[11][17] = 0

        self.board[12][8] = 0
        self.board[12][10] = 0
        self.board[12][12] = 0
        self.board[12][14] = 0
        self.board[12][16] = 0