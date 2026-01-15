from z3 import ArithRef, Solver, Int, Distinct, And
from sudoku import Sudoku
from enum import Enum


class SudokuType(Enum):
    Classic = 1
    AntiKnight = 2
    Windoku = 3
    Nonconsecutive = 4
    Center = 5


def default_constraints(s: Solver, matrix) -> None:
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


def known_value_constraints(
    s: Solver, sudoku: Sudoku, matrix: list[list[ArithRef]]
) -> None:
    # copy all values from board to the solver's possible values
    for x, row in enumerate(sudoku.board):
        for y, field in enumerate(row):
            if field is not None:
                # don't use matrix[x][y] = field it will be bad if you try to
                # query results
                s.add(matrix[x][y] == field)


def center_constraints(s: Solver, matrix: list[list[ArithRef]]) -> None:
    s.add(Distinct([matrix[i * 3 + 1][j * 3 + 1] for i in range(3) for j in range(3)]))


def non_consecutive_constraints(s: Solver, matrix: list[list[ArithRef]]) -> None:
    for x in range(8):
        for y in range(8):
            # Two horizontally adjacent number cannot be consecutive
            s.add(matrix[x][y] != matrix[x][y + 1] + 1)
            s.add(matrix[x][y] != matrix[x][y + 1] - 1)
            # Two vertically adjacent number cannot be consecutive
            s.add(matrix[x][y] != matrix[x + 1][y] + 1)
            s.add(matrix[x][y] != matrix[x + 1][y] - 1)


def gen_knight_jumps(x: int, y: int) -> list[tuple[int, int]]:
    offsets = ((1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, 2))
    output = []
    for offset in offsets:
        x_offset, y_offset = offset
        new_x = x + x_offset
        new_y = y + y_offset
        if new_x < 9 and new_x >= 0 and new_y < 9 and new_y >= 0:
            output.append((new_x, new_y))
    return output


def knight_constraints(s: Solver, matrix: list[list[ArithRef]]) -> None:
    for x in range(9):
        for y in range(9):
            possible_jumps = gen_knight_jumps(x, y)
            [s.add(matrix[x][y] != matrix[new_x][new_y]) for new_x, new_y in possible_jumps]

def windoku_constraints(s: Solver, matrix: list[list[ArithRef]]) -> None:
    for i in range(2):
        for j in range(2):
            s.add(Distinct([matrix[i*4+x+1][j*4+y+1] for x in range(3) for y in range(3)]))
    

def solve(sudoku: Sudoku, type: SudokuType):
    """Solve the sudoku

    The function solves the sudoku with z3-solver, then returns a new Sudoku
        object as the solved sudoku

    Args:
        sudoku: The sudoku that is needs to be solved

    Returns:
        A solved sudoku
    """
    s = Solver()
    matrix: list[list[ArithRef]] = [
        [Int(f"{x}{y}") for x in range(9)] for y in range(9)
    ]

    # default rules for sudoku
    default_constraints(s, matrix)
    known_value_constraints(s, sudoku, matrix)

    match type:
        case SudokuType.Center:
            center_constraints(s, matrix)
        case SudokuType.Nonconsecutive:
            non_consecutive_constraints(s, matrix)
        case SudokuType.AntiKnight:
            knight_constraints(s, matrix)
        case SudokuType.Windoku:
            windoku_constraints(s, matrix)

    # TODO: apply the check weather it is solvable
    print("="*10)
    print(s.check())
    print("="*10)
    model = s.model()

    # copy the values of the solved sudoku to the object
    solved_sudoku = Sudoku()
    for x, row in enumerate(matrix):
        for y, field in enumerate(row):
            value = model.eval(field).as_long()
            solved_sudoku.set_field(x, y, value)

    return solved_sudoku
