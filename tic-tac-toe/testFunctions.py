from tictactoe import initial_state, player, actions, result, winner, terminal, utility

board = initial_state()

board[0][0] = "O"
board[0][1] = "O"
board[0][2] = "X"
board[1][0] = "X"
board[1][1] = "X"
board[1][2] = "O"
board[2][0] = "O"
board[2][1] = "X"
board[2][2] = "X"

userturn = player(board)
possibilities = actions(board)
winnerWho = winner(board)
finish = terminal(board)
print(finish)