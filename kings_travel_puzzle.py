import numpy as np

np.set_printoptions(precision = 2, suppress = True)


def num_paths_king(n,m):
    
    board = np.zeros((n,m))

    for x in range(0,n):
        board[x][0] = 1
    
    for y in range(0,m):
        board[0][y] = 1

    for x in range(1,n):
        for y in range(1,m):
            board[x][y] = board[x-1][y] + board[x][y-1] + board[x-1][y-1]

    return board[n-1][m-1]


def num_paths_king_del_square(x,y):
    
    board = np.zeros((8,8))

    board[0][0] = 1

    for i in range(0,8):
        for j in range(0,8):
            if (i,j) == (0,0):
                pass
            elif (i,j) == (x,y):
                board[i][j] = 0
            elif i == 0:
                board[i][j] = board[i][j-1]
            elif j == 0:
                board[i][j] = board[i-1][j]
            else:
                board[i][j] = board[i-1][j] + board[i][j-1] + board[i-1][j-1]

    return board[7][7]


def print_del_grid():
    paths = []
    for x in range(0,8):
        row = []
        for y in range(0,8):
            row.append(num_paths_king_del_square(x,y))
        paths.append(row)
        print(row)


def num_paths_rook(n,m):
    
    board = np.zeros((n,m))
    board[0][0] = 1

    for i in range(1,15):
        for j in range(0,1+i):
            try:
                board[i-j][j] = board[:i-j].sum(axis=0)[j] + sum(board[i-j][:j])
            except:
                pass
    
    print(board)
    print(board[7][7])
