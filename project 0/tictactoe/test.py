from tictactoe import *

EMPTY = None
X = "X"
O = "O"
empty_board = [[EMPTY, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY],
               [EMPTY, EMPTY, EMPTY]]

board = [[X, O, EMPTY],
         [EMPTY, X, O],
         [EMPTY, X, EMPTY]]

print(result(empty_board, minimax(empty_board)))
