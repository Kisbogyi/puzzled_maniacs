from z3 import ArithRef,Solver,Int,Distinct,And,Or,sat
from sudoku import Sudoku
from solver import solve
import random, copy

board = [
        [9,8,7,4,3,5,6,1,2],
        [2,5,1,7,6,9,8,3,4],
        [6,4,3,1,8,2,5,7,9],
        [7,3,9,8,2,1,4,5,6],
        [8,6,5,9,4,3,7,2,1],
        [4,1,2,6,5,7,3,9,8],
        [1,9,4,5,7,8,2,6,3],
        ### replace the following line with Nones to get a non-unique sudoku
        [5,2,8,3,9,6,1,4,7],
        #9*[None],
        9*[None],
    ]

sudoku: Sudoku = Sudoku(board=board)
"""
9 8 7   4 3 5   6 1 2   
2 5 1   7 6 9   8 3 4   
6 4 3   1 8 2   5 7 9   

7 3 9   8 2 1   4 5 6   
8 6 5   9 4 3   7 2 1   
4 1 2   6 5 7   3 9 8   

1 9 4   5 7 8   2 6 3   
5 2 8   3 9 6   1 4 7   
3 7 6   2 1 4   9 8 5  
"""
def create_basic_matrix_and_solver(board: list[list[int]]):
    matrix: list[list[ArithRef]] = [
        [Int(f"{x}{y}") for x in range(9)] for y in range(9)
    ]
    s = Solver()
    # copy all values from board to the solver's possible values
    for x,row in enumerate(board):
        for y,field in enumerate(row):
            if field is not None:
                # don't use matrix[x][y] = field it will be bad if you try to
                # query results
                s.add(matrix[x][y] == field)
    # distinct numbers in every row from 1 to 9
    for i in range(9):
        s.add(Distinct(matrix[i]))
        for j in range(9):
            s.add(And(1 <= matrix[i][j],matrix[i][j] <= 9))
    # distinct numbers in every column
    # all numbers are from 1 to 9 so don't need that constraint again
    for row in range(9):
        column = [matrix[column][row] for column in range(9)]
        s.add(Distinct(column))
    # Distinct values in every 3 by 3 box
    for i in range(3):
        for j in range(3):
            s.add(
                Distinct(
                    [matrix[i * 3 + x][j * 3 + y] for x in range(3) for y in range(3)]
                )
            )
    return matrix, s


matrix, s = create_basic_matrix_and_solver(board) 
## now it should find the sudoku in a fraction of a second.
## Thus,I can start implementing methods of removal
## begin slop
def is_unique(board):
    matrix, s = create_basic_matrix_and_solver(board)
    # First solution
    if s.check() != sat:
        return False
    m1 = s.model()
    # Build difference constraint
    diff = []
    for r in range(9):
        for c in range(9):
            diff.append(matrix[r][c] != m1[matrix[r][c]].as_long())
    # Second solver with "must differ" rule
    s2 = Solver()
    s2.add(s.assertions())
    s2.add(Or(diff))
    return s2.check() != sat   # UNIQUE iff no second solution exists

def remove_a_cell(puzzle: Sudoku):
    assert is_unique(puzzle.board)
    # Collect all filled cells
    filled_cells = [(r, c) for r in range(9) for c in range(9)
                    if puzzle.board[r][c] is not None]

    random.shuffle(filled_cells)   # randomize selection

    # Try removing each possible cell once
    for (r, c) in filled_cells:
        new_board = [row[:] for row in puzzle.board]
        new_board[r][c] = None

        if is_unique(new_board):
            # SUCCESS
            puzzle.board = new_board
            return puzzle

    # No removable cell found
    return None
## end slop

mostly_empty = copy.copy(sudoku)
removed = remove_a_cell(sudoku)
i = 1
print(removed)
print("meeewo")
while removed:
    print(f"removed {i}")
    mostly_empty = removed
    removed = remove_a_cell(removed)
    i += 1

print(mostly_empty)