from z3 import ArithRef,Solver,Int,Distinct,And,Or,sat
from our_sudoku import OurSudoku
from our_solver import solve
## uv pip install py-sudoku
from sudoku import Sudoku

board = [
        [9,8,7,4,3,5,6,1,2],
        [2,5,1,7,6,9,8,3,4],
        [6,4,3,1,8,2,5,7,9],
        [7,3,9,8,2,1,4,5,6],
        [8,6,5,9,4,3,7,2,1],
        [4,1,2,6,5,7,3,9,8],
        [1,9,4,5,7,8,2,6,3],
        ### replace the following line with Nones to get a non-unique sudoku
        #[5,2,8,3,9,6,1,4,7],
        9*[None],
        9*[None],
    ]

sudoku: OurSudoku = OurSudoku(board=board)
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
matrix: list[list[ArithRef]] = [
    [Int(f"{x}{y}") for x in range(9)] for y in range(9)
]
s = Solver()

# copy all values from board to the solver's possible values
for x,row in enumerate(sudoku.board):
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

## now it should find the sudoku in a fraction of a second.
## Thus,I can start implementing methods of removal
# Checking whether two Z3 models are equal SLOP WARNING https://codingtechroom.com/question/-check-model-uniqueness-z3
### This was made with help from Copilot
# Solve once
result = s.check()
if result != sat:
    print("Sudoku has no solution.")
    exit(0)

m1 = s.model()

# Build "difference constraint":
# There must exist at least one (x,y) such that model[x][y] != matrix[x][y]
diff_constraints = []

for x in range(9):
    for y in range(9):
        v = m1[matrix[x][y]]
        diff_constraints.append(matrix[x][y] != v.as_long())

# Create a second solver with all original constraints + "solutions must differ"
s2 = Solver()
s2.add(s.assertions())        # copy all sudoku rules + fixed cells
s2.add(Or(diff_constraints))  # enforce different solution

# Check second model
result2 = s2.check()

if result2 == sat:
    print("Sudoku does NOT have a unique solution.")
else:
    print("Sudoku has a UNIQUE solution.")
### end AI SLOP


## this only works for traditional sudokus, which is fine:P
official_pysudoku = Sudoku(3,3,board)
print(official_pysudoku.get_difficulty())

## a more "efficient" solution might be to check values by hand
## but then again,Z3 runs on a low level
## so maybe the overhead is quite small compared to recursive review