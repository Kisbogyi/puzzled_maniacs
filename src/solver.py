from z3 import ArithRef, Solver, Int, Distinct, And
from sodoku import Sodoku


def solve(sodoku: Sodoku):
    """Solve the sodoku

    The function solves the sodoku with z3-solver, then returns a new Sodoku
        object as the solved sodoku

    Args:
        sodoku: The sodoku that is needs to be solved

    Returns:
        A solved sodoku
    """
    matrix: list[list[ArithRef]] = [
        [Int(f"{x}{y}") for x in range(9)] for y in range(9)
    ]
    s = Solver()

    # copy all values from board to the solver's possible values
    for x, row in enumerate(sodoku.board):
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

    # copy the values of the solved sodoku to the object
    solved_sodoku = Sodoku()
    for x, row in enumerate(matrix):
        for y, field in enumerate(row):
            value = model.eval(field).as_long()
            solved_sodoku.set_field(x, y, value)

    return solved_sodoku
