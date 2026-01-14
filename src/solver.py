from z3 import ArithRef, Solver, Int, Distinct, And
from sudoku import OurSudoku


def solve(sudoku: OurSudoku):
    """Solve the sudoku

    The function solves the sudoku with z3-solver, then returns a new sudoku
        object as the solved sudoku

    Args:
        sudoku: The sudoku that is needs to be solved

    Returns:
        A solved sudoku
    """
    matrix: list[list[ArithRef]] = [
        [Int(f"{x}{y}") for x in range(9)] for y in range(9)
    ]
    s = Solver()

    # copy all values from board to the solver's possible values
    for x, row in enumerate(sudoku.board):
        for y, field in enumerate(row):
            if field is not None:
                # don't use matrix[x][y] = field it will be bad if you try to
                # query results
                s.add(matrix[x][y] == field)

    # distinct numbers in every row from 1 to 9
    for i in range(9):
        s.add(Distinct(matrix[i]))
        for j in range(9):
            s.add(And(1 <= matrix[i][j], matrix[i][j] <= 9))

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

    # TODO: apply the check weather it is solvable
    s.check()
    model = s.model()

    # copy the values of the solved sudoku to the object
    solved_sudoku = OurSudoku()
    for x, row in enumerate(matrix):
        for y, field in enumerate(row):
            value = model.eval(field).as_long()
            solved_sudoku.set_field(x, y, value)

    return solved_sudoku
