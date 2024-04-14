# Function to check if all elements of the board[][] array store value in the range[1, 9]
def isinRange(board):
    N = 9
    for i in range(0, N):
        for j in range(0, N):
            if (board[i][j] <= 0) or (board[i][j] > 9):
                return False
    return True

def isValidSudoku(board):
    N = 9
    if isinRange(board) == False:
        return False
    unique = [False] * (N + 1)

    for i in range(0, N):
        for m in range(0, N + 1):
            unique[m] = False

        for j in range(0, N):
            Z = board[i][j]
            if unique[Z] == True:
                return False

            unique[Z] = True

    for i in range(0, N):
        for m in range(0, N + 1):
            unique[m] = False
        for j in range(0, N):
            Z = board[j][i]

            if unique[Z] == True:
                return False

            unique[Z] = True

    for i in range(0, N - 2, 3):
        for j in range(0, N - 2, 3):
            for m in range(0, N + 1):
                unique[m] = False

            for k in range(0, 3):
                for l in range(0, 3):
                    X = i + k
                    Y = j + l
                    Z = board[X][Y]
                    if unique[Z] == True:
                       return False
                    unique[Z] = True
    return True

def is_valid_sudoku(grid):

    for row in grid:
        if not is_valid_unit(row):
            return False

    for col in zip(*grid):
        if not is_valid_unit(col):
            return False

    for i in (0, 3, 6):
        for j in (0, 3, 6):
            unit = [grid[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            if not is_valid_unit(unit):
                return False
    return True

def is_valid_unit( unit):
    unit = [i for i in unit if i != 0]
    return len(unit) == len(set(unit))

def is_num_valid(puzzle, i, j, num):
    for k in range(9):
        if puzzle[i][k] == num:
            return False

    for k in range(9):
        if puzzle[k][j] == num:
            return False

    row_start = i // 3 * 3
    col_start = j // 3 * 3
    for k in range(3):
        for l in range(3):
            if puzzle[row_start + k][col_start + l] == num:
                return False
    return True

if __name__ == "__main__":
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    if isValidSudoku(board):
        print("Valid")
    else:
        print("Not Valid")

    if is_valid_sudoku(board):
        print("Valid")
    else:
        print("Not Valid")