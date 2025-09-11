from minesweeper import Minesweeper

board = []
for i in range(5):
    row = []
    for j in range(5):
        if i % 2 == 0:
            row.append(True)
        else:
            row.append(False)
    board.append(row)


test = Minesweeper()

count = test.nearby_mines((0,3))

print(count)