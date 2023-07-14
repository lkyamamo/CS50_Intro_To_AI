from tictactoe import *

board = initial_state()

for i in range(3):
    board[0][i] = "X"

print(board)
print(winner(board))

board = initial_state()

board[0][0] = "O"
board[1][1] = "O"
board[2][2] = "O"

print(winner(board))

board = initial_state()

for i in range(3):
    board[i][0] = "X"

print(winner(board))